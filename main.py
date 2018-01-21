import prman
import os


DEFAULT_IMAGE_EXT = 'tiff'
DEFAULT_IMAGE_SIZE = 512


class RenderViewer(object):
    def __init__(self, output_dir=None):
        super(RenderViewer, self).__init__()
        self.output_dir = output_dir or os.getcwd()
        self.render_color = [.5, .5, .5]
        self.render_log = ''
        self.rib_full_path = self.get_rib_full_path()
        self.image_full_path = self.get_image_full_path()
        self.render_log_full_path = os.path.join(self.output_dir, 'render.log')

    def get_image_full_path(self):
        rib_file_dir = os.path.dirname(self.rib_full_path)
        rib_file_name = os.path.basename(self.rib_full_path).split('.')[0]
        image_file_path = os.path.join(rib_file_dir, '{0}.{1}'.format(rib_file_name, DEFAULT_IMAGE_EXT))
        return image_file_path

    def get_rib_full_path(self):
        rib_full_path = os.path.join(self.output_dir, 'default.rib')
        return rib_full_path

    def set_render_colr(self, color):
        self.render_color = color

    def generate_rib_file(self, rib_full_path=''):
        if rib_full_path:
            self.rib_full_path = rib_full_path
        image_file_path = self.get_image_full_path()

        ri = prman.Ri()
        rendertarget = self.rib_full_path
        ri.Begin(rendertarget)
        ri.Display(image_file_path, DEFAULT_IMAGE_EXT, 'rgba', {'string compression': 'pixarlog'})
        ri.Format(DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE, 1)
        ri.Projection(ri.PERSPECTIVE, {ri.FOV: 45})
        ri.Translate(0, 0, 20)
        ri.Rotate(-90, 1, 0, 0)
        ri.WorldBegin()
        ri.Bxdf('PxrDisney', 'PxrDisney1', {'color baseColor': self.render_color}, 'PxrValidateBxdf')
        ri.Geometry('teapot')
        ri.WorldEnd()
        ri.End()

    def render_to_disk(self):
        render_cmd = 'prman -loglevel 4 -logfile {0} {1}'.format(self.render_log_full_path, self.rib_full_path)
        os.system(render_cmd)
        return render_log_file

    def get_render_log_data(self):
        render_log = ''
        with open(self.render_log_full_path, 'r') as log_file:
            render_log = log_file.readlines()
        return render_log


if __name__ == '__main__':
    rib_file_path = '/tmp/default.rib'

    render_viewer = RenderViewer()
    #   Generate rib file.
    render_viewer.generate_rib_file()

    #   Render to disk.
    render_log_file = render_viewer.render_to_disk()
    print render_log_file

    #   Print render log.
    render_log = render_viewer.get_render_log_data()
    print render_log

