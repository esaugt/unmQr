##modelo de sitios

from django.db import models

class Bloque(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre del bloque', max_length=100, null=False, blank=False)
    funciones = models.CharField('Funciones del Bloque', max_length=100)
    nombre_encargado = models.CharField('Nombre del encargado', max_length=100, blank=True)
    numero_planta = models.IntegerField('Número de plantas')
    horario_bloque = models.CharField('Horarios', max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    ubicacion = models.TextField('iframe', blank=True, null=False)
    imagen = models.ImageField(upload_to='bloque_imagenes/', null=True, blank=True)


    class Meta:
        verbose_name = 'Bloque'
        verbose_name_plural = 'Bloques'

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        super(Bloque, self).save(*args, **kwargs)
        
        # Verificar si el bloque tiene un número válido de plantas
        if self.numero_planta > 0:
            # Obtener las plantas existentes asociadas a este bloque
            plantas_existentes = Planta.objects.filter(bloque=self)

            if self.numero_planta > plantas_existentes.count():
                # Crear plantas adicionales si se ha aumentado el número de plantas
                for numero_planta in range(plantas_existentes.count() + 1, self.numero_planta + 1):
                    Planta.objects.create(numero_planta=numero_planta, bloque=self)
            elif self.numero_planta < plantas_existentes.count():
                # Eliminar plantas si se ha reducido el número de plantas
                plantas_excedentes = plantas_existentes[self.numero_planta:]
                for planta in plantas_excedentes:
                    planta.delete()

class Sitio(models.Model):
    id = models.AutoField(primary_key= True)
    nombre = models.CharField('Nombre del Sitio',max_length=100,null = False ,blank= False)
    bloque = models.ForeignKey('Bloque', on_delete=models.PROTECT, default="", blank= False)
    planta = models.ForeignKey('Planta', on_delete=models.PROTECT, default="", blank=False, null=True)
    horario = models.CharField('Horario de atencion',max_length=100, blank= True)
    imagen = models.ImageField(upload_to='bloque_imagenes/', null=True, blank=True)
    planta = models.ForeignKey('Planta', on_delete=models.CASCADE, default="", blank=False, null=True)
    descripcion = models.TextField('Descripción del Sitio', null=True, blank=True)
    aulas=models.TextField(null=True, blank=True)
    nombre_encargado = models.CharField('Nombre del Encargado', max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Sitio'
        verbose_name_plural = 'Sitios'
    
    def __str__(self):
        return self.nombre


class Planta(models.Model):
    numero_planta = models.IntegerField('Número de planta')
    bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE, related_name='plantas')
    # Otros campos relacionados con la planta, si los necesitas

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'

    def __str__(self):
        return f"Planta {self.numero_planta} - {self.bloque.nombre}"

    def save(self, *args, **kwargs):
        # Diccionario que mapea el número de planta al nombre del piso
        nombres_pisos = {
            1: "Planta Baja",
            2: "Primer Piso",
            3: "Segundo Piso",
            4: "Tercer Piso",
            5: "Cuarto Piso",
        }

        # Verificar si el número de planta está en el diccionario
        if self.numero_planta in nombres_pisos:
            # Establecer el nombre del piso basado en el número de planta
            self.nombre_piso = nombres_pisos[self.numero_planta]
        
        # Llamar al método save() del modelo padre para guardar los cambios
        super(Planta, self).save(*args, **kwargs)