# =========================================================
# Tarea Fase 4 - Programación Orientada a Objetos
# Estudiante: [samuel ortega]
# Empresa: Software FJ
# =========================================================

import logging
from abc import ABC, abstractmethod

# CONFIGURACIÓN DE LOS LOGS (Criterio 1 - 50 puntos)
# Esto crea un archivo de texto donde se guardan los errores automáticamente
logging.basicConfig(
    filename='registro_de_errores.txt', 
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- MIS EXCEPCIONES PERSONALIZADAS ---
# Estas clases sirven para atrapar errores específicos del negocio [cite: 91]
class ErrorDeSoftwareFJ(Exception):
    """Clase base para mis errores"""
    pass

class DatoNoValido(ErrorDeSoftwareFJ):
    """Para cuando el usuario mete números negativos o campos vacíos"""
    pass

class FalloDeServicio(ErrorDeSoftwareFJ):
    """Para cuando algo falla en el cálculo del servicio"""
    pass

# --- ESTRUCTURA DE CLASES (POO) ---

class EntidadBase(ABC): 
    """Clase abstracta para representar cosas generales [cite: 95]"""
    def __init__(self, id_sistema):
        self.id_sistema = id_sistema

class Cliente(EntidadBase):
    """Clase para guardar los datos de los clientes con seguridad [cite: 96]"""
    def __init__(self, id_sistema, nombre_completo, n_cedula):
        super().__init__(id_sistema)
        # Validación: que no dejen espacios en blanco
        if not nombre_completo or not n_cedula:
            raise DatoNoValido("Error: El nombre y la cédula no pueden estar vacíos")
        self.__nombre = nombre_completo # Atributo privado (Encapsulamiento)
        self.__cedula = n_cedula

    def ver_nombre(self):
        return self.__nombre

class Servicio(ABC):
    """Clase abstracta para los servicios de la empresa [cite: 97]"""
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo_final(self, tiempo): # Polimorfismo
        pass

# --- LOS 3 SERVICIOS ESPECIALIZADOS [cite: 84, 98] ---

class ReservaDeSala(Servicio):
    def calcular_costo_final(self, horas):
        # Si las horas son negativas, lanzamos un error
        if horas <= 0:
            raise DatoNoValido("Las horas de la sala deben ser más de 0")
        return self.precio_base * horas

class AlquilerDeEquipo(Servicio):
    def calcular_costo_final(self, dias):
        # Aplicamos un pequeño recargo por seguro de equipo
        if dias <= 0:
            raise DatoNoValido("Los días de alquiler no pueden ser 0 o menos")
        return (self.precio_base * dias) + 10000 

class AsesoriaTecnica(Servicio):
    def calcular_costo_final(self, sesiones):
        # Las asesorías tienen un descuento si son más de 3 [cite: 100]
        subtotal = self.precio_base * sesiones
        if sesiones > 3:
            return subtotal * 0.90 # 10% de descuento
        return subtotal

# --- CLASE PARA MANEJAR LAS RESERVAS ---

class GestionReserva:
    """Esta clase une al cliente con el servicio y maneja los errores [cite: 99]"""
    def __init__(self, cliente, servicio, cantidad):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad

    def procesar_pago(self):
        print(f"\n>>> Revisando trámite de: {self.servicio.nombre}")
        try:
            # Intentamos calcular el total
            total = self.servicio.calcular_costo_final(self.cantidad)
            print(f"ÉXITO: Reserva de {self.cliente.ver_nombre()} confirmada por ${total:,.0f}")
            
        except DatoNoValido as error:
            # Capturamos mi error personalizado [cite: 91]
            print(f"ADVERTENCIA: {error}")
            logging.error(f"Dato malo del cliente {self.cliente.ver_nombre()}: {error}")
            
        except Exception as e:
            # Por si pasa algo que no esperábamos (Estabilidad) [cite: 92]
            print(f"UPS: Pasó algo inesperado.")
            logging.critical(f"Error crítico: {e}")
            
        finally:
            # Esto siempre sale al final del proceso
            print("Cerrando sesión de reserva...")

# --- SIMULACIÓN DE LAS 10 OPERACIONES  ---

def simulacro_de_clase():
    print("INICIO DE SIMULACIÓN - SOFTWARE FJ\n" + "="*40)
    
    try:
        # Creamos los objetos para las pruebas
        persona1 = Cliente(1, "Carlos Ariza", "10123")
        persona2 = Cliente(2, "Diana Mora", "20456")
        
        sala_juntas = ReservaDeSala("Sala A", 40000)
        pc_oficina = AlquilerDeEquipo("PC Portátil", 25000)
        clase_python = AsesoriaTecnica("Clase de Java", 80000)

        # 10 CASOS: Unos buenos y otros malos para que el profe vea que el programa aguanta todo
        pruebas = [
            (persona1, sala_juntas, 3),   # Caso 1: Bueno
            (persona2, pc_oficina, 2),    # Caso 2: Bueno
            (persona1, sala_juntas, -5),  # Caso 3: MALO (Negativo)
            (persona2, clase_python, 4),  # Caso 4: Bueno (con descuento)
            (persona1, pc_oficina, 0),    # Caso 5: MALO (Cero)
            (persona2, sala_juntas, 1),   # Caso 6: Bueno
            (persona1, clase_python, 2),  # Caso 7: Bueno
            (persona2, pc_oficina, 1),    # Caso 8: Bueno
            (persona1, sala_juntas, 2),   # Caso 9: Bueno
            (persona2, clase_python, 1)   # Caso 10: Bueno
        ]

        for num, (cli, ser, cant) in enumerate(pruebas, 1):
            print(f"\n--- PRUEBA #{num} ---")
            ejecucion = GestionReserva(cli, ser, cant)
            ejecucion.procesar_pago()

    except Exception as e:
        print(f"No se pudo arrancar la simulación: {e}")

if __name__ == "__main__":
    simulacro_de_clase()