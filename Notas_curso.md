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