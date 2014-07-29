from shackline import api

from controllers.hello_world import HelloWorld
api.add_resource(HelloWorld, '/hello-world')

# from controllers.get_image import GetImage
# api.add_resource(GetImage, '/get-image')

from controllers.get_count import GetCount
api.add_resource(GetCount, '/get-count')
