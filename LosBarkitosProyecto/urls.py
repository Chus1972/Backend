from django.conf.urls import patterns, include, url
from django.contrib import admin

from LosBarkitosApp.views import llegada
from LosBarkitosApp.views import barcasFuera
from LosBarkitosApp.views import primeraLibre
from LosBarkitosApp.views import salidaBarca
from LosBarkitosApp.views import llegadaBarca
from LosBarkitosApp.views import disponible
from LosBarkitosApp.views import noDisponible
from LosBarkitosApp.controlViaje import registroBarca, listadoViajes
from LosBarkitosApp.controlVendedor import ventaVendedor
from LosBarkitosApp.views import resetear
from LosBarkitosApp.controlReserva import reserva, reserva_fuera

#router = routers.DefaultRouter()
#router.register(r'barca', BarcaViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LosBarkitosProyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^llegada/', include(router.urls)),
    url(r'^llegada/$', llegada),
    url(r'^fuera/', barcasFuera),
    url(r'^primera_libre/', primeraLibre),
    url(r'^salida/(Rio|Electrica|Whaly|Gold)/$', salidaBarca),
    url(r'^llegada/(Rio|Electrica|Whaly|Gold)/$', llegadaBarca),
    url(r'^disponible/([1-9]|1[0-9]|20)/$', disponible),
    url(r'^no_disponible/([1-9]|1[0-9]|20)/$', noDisponible),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^barcas/$', 'LosBarkitosApp.views.barcas'),
    url(r'^registro_barca/([1-5])/([1-9][0-9]*)/([123])/([12345])/$', registroBarca),
    url(r'^venta_vendedor/([1-9])/$', ventaVendedor),
    url(r'^resetear_barcas/$', resetear),
    url(r'^reserva/(Rio|Electrica|Whaly|Gold)/([123])$', reserva),
    url(r'^reserva_fuera/([0-9]+)/$', reserva_fuera),
    url(r'^listado_viaje/(?P<tipo>[01234])/(?P<pv>[0123])/(?P<vend>[01234])/$', listadoViajes),

)
