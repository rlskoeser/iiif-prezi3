
from ..loader import monkeypatch_schema
from ..skeleton import (Annotation, AnnotationPage, Canvas, Manifest,
                        ResourceItem, ServiceItem, ServiceItem1)


class CreateCanvasFromIIIF:
    # should probably be added to canvas helpers

    def create_canvas_from_iiif(self, url, **kwargs):
        """Create a canvas from a IIIF Image URL.

        Creates a canvas from a IIIF Image service passing any
        kwargs to the Canvas. Returns a Canvas object

        """
        canvas = Canvas(**kwargs)

        body = ResourceItem(id="http://example.com", type="Image")
        infoJson = body.set_hwd_from_iiif(url)

        # Will need to handle IIIF 2...
        if 'type' not in infoJson:
            # Assume v2

            # V2 profile contains profile URI plus extra features
            profile = ''
            for item in infoJson['profile']:
                if isinstance(item, str):
                    profile = item
                    break

            service = ServiceItem1(id=infoJson['@id'], profile=profile, type="ImageService2")
            body.service = [service]
            body.id = f'{infoJson["@id"]}/full/full/0/default.jpg'
            body.format = "image/jpeg"
        else:
            service = ServiceItem(id=infoJson['id'], profile=infoJson['profile'], type=infoJson['type'])
            body.service = [service]
            body.id = f'{infoJson["id"]}/full/max/0/default.jpg'
            body.format = "image/jpeg"

        annotation = Annotation(motivation='painting', body=body, target=canvas.id)

        annotationPage = AnnotationPage()
        annotationPage.add_item(annotation)

        canvas.add_item(annotationPage)
        canvas.set_hwd(infoJson['height'], infoJson['width'])

        return canvas

    def make_canvas_from_iiif(self, url, **kwargs):
        canvas = self.create_canvas_from_iiif(url, **kwargs)

        self.add_item(canvas)
        return canvas


monkeypatch_schema(Manifest, [CreateCanvasFromIIIF])
