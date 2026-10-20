"""Regression checks runnable without installing Home Assistant."""
import ast
import asyncio
import copy
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / 'custom_components/lazar_hi20'
spec = importlib.util.spec_from_file_location('values', COMPONENT / 'values.py')
values = importlib.util.module_from_spec(spec)
spec.loader.exec_module(values)

def coordinator_method(name):
    tree = ast.parse((COMPONENT / 'coordinator.py').read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    method = next(n for n in cls.body if getattr(n, 'name', None) == name)
    method.decorator_list = []
    method.name = "method_under_test"
    module = ast.fix_missing_locations(ast.Module(body=[method], type_ignores=[]))
    ns = {'room_temperature': values.room_temperature, 'DATA_URL':'https://example.invalid', 'ConfigEntryAuthFailed':RuntimeError}
    exec(compile(module, '<coordinator test>', 'exec'), ns)
    return ns["method_under_test"]

class TemperatureTests(unittest.TestCase):
    def test_api_scaling(self):
        for raw, expected in [(215,21.5),('215',21.5),(-55,-5.5),(0,0)]:
            self.assertAlmostEqual(values.numeric_value(raw,.1), expected)

    def test_missing_and_invalid(self):
        for raw in [None,-9999,'-9999',True,False,'unknown','unavailable','NaN',float('inf'),{},[]]:
            self.assertIsNone(values.numeric_value(raw,.1), repr(raw))

    def test_units(self):
        for raw, unit, expected in [('21.5','°C',21.5),(68,'°F',20),(293.15,'K',20)]:
            self.assertAlmostEqual(values.room_temperature(raw,unit),expected)
        self.assertIsNone(values.room_temperature(20,None))

    def test_room_source_is_live(self):
        state=SimpleNamespace(state='21.5',attributes={'unit_of_measurement':'°C'})
        owner=SimpleNamespace(room_sensor_entity='sensor.room',hass=SimpleNamespace(states=SimpleNamespace(get=lambda _:state)))
        read=coordinator_method('room_temperature')
        self.assertEqual(read(owner),21.5)
        state.state='22'
        self.assertEqual(read(owner),22)
        state.state='unavailable'
        self.assertIsNone(read(owner))
        owner.room_sensor_entity=None
        self.assertIsNone(read(owner))

    def test_fetch_does_not_overwrite_setpoints(self):
        payload={'params':{'cricuits':[{'troomsetheat':230,'troomsetcool':250}]}}
        original=copy.deepcopy(payload)
        class Response:
            headers={'Content-Type':'application/json'}
            async def __aenter__(self): return self
            async def __aexit__(self,*args): pass
            def raise_for_status(self): pass
            async def json(self): return payload
        owner=SimpleNamespace(_has_valid_cookie=lambda:True,session=SimpleNamespace(get=lambda *a,**kw:Response()),room_sensor_entity='sensor.room',hass=SimpleNamespace(states=SimpleNamespace(get=lambda _:SimpleNamespace(state='21.5'))))
        result=asyncio.run(coordinator_method('_fetch_and_parse')(owner))
        self.assertEqual(result,original)
        self.assertEqual(payload,original)

    def test_room_sensor_and_setpoint_have_separate_sources(self):
        tree=ast.parse((COMPONENT/'const.py').read_text())
        assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SENSOR_TYPES' for t in n.targets))
        ns={'UnitOfTemperature':SimpleNamespace(CELSIUS='°C'),'UnitOfPower':SimpleNamespace(WATT='W'),'PERCENTAGE':'%','SensorDeviceClass':SimpleNamespace(TEMPERATURE='temperature',POWER='power')}
        exec(compile(ast.Module(body=[assignment],type_ignores=[]),'<const test>','exec'),ns)
        configs=ns['SENSOR_TYPES']
        self.assertEqual(configs['troomsetheat']['source'],'room')
        self.assertNotIn('path',configs['troomsetheat'])
        self.assertEqual(configs['room_target_heat']['scale'],.1)

if __name__=='__main__': unittest.main()
