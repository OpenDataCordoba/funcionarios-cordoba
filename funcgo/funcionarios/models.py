from django.db import models


class Institucion(models.Model):
    ''' Provincia, muni, legislatura, etc '''
    nombre = models.CharField(max_length=90)

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    ''' cargo específico dentro de una institucion '''
    nombre = models.CharField(max_length=90)
    depende_de = models.ForeignKey('self', null=True,
                                    blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='dependientes',
                                    help_text='Cargo del cual depende directa o indirectamente')

    def __str__(self):
        return self.nombre


class Funcionario(models.Model):
    ''' una persona que ejerce o ejerció un cargo en una institucion pública '''
    nombres = models.CharField(max_length=190)
    apellidos = models.CharField(max_length=190, null=True, blank=True)

    # datos extras que podríamos tener y son de utilidad
    dni = models.CharField(max_length=20, null=True, blank=True)
    cuit = models.CharField(max_length=20, null=True, blank=True)

    @property
    def nombre(self):
        apellidos = '' if self.apellidos is None else ' {}'.format(self.apellidos)
        return '{}{}'.format(self.nombres, apellidos)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if self.cuit is not None:
            self.cuit = self.cuit.replace('-', '')
        super().save(*args, **kwargs)


class FuncionarioEnCargo(models.Model):
    ''' una persona ejerciendo un cargo '''
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='cargos')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='funcionarios')

    fecha_inicio_detectada = models.DateField(null=True, blank=True)
    fecha_fin_detectada = models.DateField(null=True, blank=True)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.funcionario, self.cargo)


class RedSocial(models.Model):
    ''' redes sociales del funcionario '''
    nombre = models.CharField(max_length=90)

    def __str__(self):
        return self.nombre


class CargoRedSocial(models.Model):
    ''' redes oficiales de las oficinas de gobienro '''
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='redes')
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='cargos')
    user_name = models.CharField(max_length=90)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return '@{}'.format(self.user_name)

class FuncionarioRedSocial(models.Model):
    ''' redes de los funcionarios '''
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='redes')
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='funcionarios')
    user_name = models.CharField(max_length=90)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return '@{}'.format(self.user_name)