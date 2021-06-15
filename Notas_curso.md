# Comandos iniciales desarrollo
$ cd cride
`docker-compose -f local.yml build` <<>> descargar isos

`docker-compose -f local.yml up` <<>> subir los servicios

`docker-compose -f local.yml ps` <<>> ver los que esta corriendo

`docker-compose -f local.yml down` <<>> Matar todos los servicios 

### resumir comandos 
`export COMPOSE_FILE=local.yml` <<>> cargar la variable local.yml
`docker-compose build` 
`docker-compose up` 
`docker-compose ps` 
`docker-compose down`

## Comandos administrativos 

`export COMPOSE_FILE=local.yml` <> primero exportamos el local.yml

`docker-compose run --rm django <comando>` <<>> --rm para que muera el contenedor

`docker-compose run --rm django python manage.py createsuperuser ` <> crear usuario admin

`docker rm -f cride_django_1 `  <<>> bajar un servicio Django

`docker-compose run --rm --service-ports django` <> subir el servicio en monitoreo otra teminal independiente

### generar migraciones 
`docker-compose run --rm django python manage.py makemigrations`

### Crear las migracion
`docker-compose run --rm django python manage.py migrate`
### Borrar base de datos
`docker-compose run --rm django python manage.py flush`

### correr pruebas test

`docker-compose run --rm django pytest`

"import ipdb; ipdb.set_trace()"  <> Ver en la terminal log y gestion

# Comandos Docker basicos

`docker container []`
`docker images []`
`docker volume []`
`docker network []`
[ls]
[rm]
[prune]
[-a]
[-q]
[--help]

## librerias pip

`pip install httpie`

`http localhost:8000/circles/`  <> genera el query
`http localhost:8000/circles/ -b` <> genera el body
`http localhost:8000/circles/ -v` <> respueta verbosa


## Debugging python 
`pip install ipdb` 

`import ipdb; ipdb.set_trace()`
## comando http terminal
registrar usuario:
`http POST localhost:8000/users/signup/ email="prueba@gmail.com" first_name=prueba last_name=hernandez password=admin123 password_confirmation=admin123 phone_number=+3102331028 username=infinity`

`http localhost:8000/circles/ -b`
`http localhost:8000/users/login/`
`http localhost:8000/users/login/ email=prueba@gmail.com password=admin123 -b`

`http localhost:8000/users/verify/ token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiaW5maW5pdHkiLCJleHAiOjE2MjI1NzMyMDMsInR5cGUiOiJlbWFpbF9jb25maXJtYXRpb24ifQ.PkeolGKjc0jsaZxwdTdxdYseB-qgJst2YPZ2UJ0l0mc"`

## en Shell_plus:
`User.objects.all()` ver usuarios
`User.objects.get(username='infinity')`  un usuario

<User: infinity>, <User: ruber>]>

`User.objects.all().delete()` Borrar los usuarios
`Membership.objects.first().is_admin` 
`Membership.objects.all().values('user','circle','is_admin')` ver miembros admin
Out[9]: <QuerySet [{'user': 7, 'circle': 25, 'is_admin': True}]>
`Token.objects.get(user__username='infinity')` <> Token de usuario
`u = User.objects.first()` <> cargar primer usuario
`c = Circle.objects.first()`
`Invitation.objects.create(issued_by=u, circle=c)` <> crea invitacion

Crear Membership
``` 
user = User.objects.get(username='ruberh')
circle = Circle.objects.get(slug_name='unam-fciencias')

m = Membership.objects.create(
    user=user, 
    profile=user.profile, 
    circle=circle, 
    is_admin=True, 
    remaining_invitations=10
)
```
ver los codigos:
`Invitation.objects.all().values_list('code')`
lista circulos:
`Circle.objects.all()`
lista invitacion:
`Invitation.objects.all()`
<QuerySet [<Invitation: #unam-fciencias: .U.MGVNS2B>, <Invitation: #unam-fciencias: HRX2929JYT>]>

`Membership.objects.all()`
<QuerySet [<Membership: @infinity at #itesm-csf>, <Membership: @infinity at #itesm-csf>, <Membership: @infinity at #platzi-limitado>, <Membership: @infinity at #platzi-Ruber>]>

`User.objects.all()`
<QuerySet [<User: ruber>, <User: ruberh>, <User: infinity>]>

`Profile.objects.all()`
<QuerySet [<Profile: ruberh>, <Profile: infinity>]>

`Token.objects.all()`
<QuerySet [<Token: 2b9c7bbffb217fd3596c2e0ae2c219034170ed9a>, <Token: 157dd9af7412d3efbe96fd40f452247aea863f1c>, <Token: 96858d772142acf73c145e12900ec2d0431f45b8>]>



# PRODUCION Docker

permsos al llave aws
`chmod 0400 CRideProduction.pem`
`sudo ssh -i CRideProduction.pem ubuntu@<ip>`
`sudo apt-get update -y`
`sudo apt-get upgrade -y`
`sudo apt-get install git`


INSTALAR DOCKER:

crear variables entorno .envn
`ls -al .envs` lista entornos
`mkdir .envs/.production`
`touch .envs/.production/.django`
`touch .envs/.production/.postgres`
`touch .envs/.production/.caddy`
pergar variables
`vim .envs/.production/.postgres`
`vim .envs/.production/.caddy` se agrega 

configura el bucket:
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')

agregar en Namecheap "www"

agregar production.py: 
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['lasmesas.club'])
construir imagenes:
`sudo docker-compose -f production.yml build`
`sudo docker-compose -f production.yml up`

probar django:
`sudo docker-compose -f production.yml run --rm django python manage.py collectstatic`
crear migraciones:
`sudo docker-compose -f production.yml run --rm django python manage.py migrate`

crar usuario
`sudo docker-compose -f production.yml run --rm django python manage.py createsuperuser`

Docker supervisor:

`sudo su`
`apt-get install supervisor`
`service supervisor restart `
`cd /etc/supervisor/conf.d/  `
`vim cride.conf  `
```
[program:cride]
command=docker-compose -f production.yml up
directory=/home/ubuntu/Curso_Django-avanzado_proyect/cride
redirect_stderr=true
autostart=true
autorestart=true
priority=10

```



