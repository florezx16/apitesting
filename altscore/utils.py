import math
from .models import RequestLog, SystemCode

def createRequestLog(instance):
    log = RequestLog(system=instance)
    log.save()
    return log

def getCodeByLog(log):
    if log:
        log_instance = RequestLog.objects.get(id=log)
    else:
        log_id = RequestLog.objects.all()[:1]
        log_instance = RequestLog.objects.get(id=log_id)
    systemCode_instance = SystemCode.objects.get(system=log_instance.system)
    return systemCode_instance.code

'''
Pc = 10MPa
Tc = 500 c~
vc = 0.0035 m^3/kg
'''

def specific_volume_liquid(pressure):
    """
    Calcula el volumen específico del líquido saturado a una presión dada.

    Fórmula usada:
    v_f(P) = vc - 0.0002462 * (10 - P)

    Donde:
    - 0.0002462 => pendiente aproximada de la recta que conecta el punto crítico (10 MPa) 
                   hacia presiones más bajas en la línea de líquido saturado.
                   (Se calcula basado en los datos del diagrama mostrado.)
    - (10 - pressure) => diferencia respecto al punto crítico, para interpolar linealmente.
    """
    result = 0.0035 - 0.0002462 * (10-pressure)
    return round(result,4)

def specific_volume_vapor(pressure):
    """
    Calcula el volumen específico del vapor saturado a una presión dada.

    Fórmula usada:
    v_g(P) = 31.53 * exp(-0.910 * P)

    Donde:
    - 31.53 [m^3/kg] => volumen específico aproximado del vapor saturado 
                        a presiones muy bajas (cercanas a 0 MPa).
    - 0.910 => constante que define qué tan rápido decae el volumen del vapor 
               al aumentar la presión.
    - exp(-0.910 * P) => comportamiento exponencial decreciente típico de la curva de vapor saturado.
    """
    result = 31.53 * math.exp(-0.910*pressure)
    return round(result,4)
