# import prman
import os


DEFAULT_IMAGE_EXT = 'tiff'
DEFAULT_IMAGE_SIZE = 512

def get_render_image_path(rib_file_path=''):
    rib_file_dir = os.path.dirname(rib_file_path)
    rib_file_name = os.path.basename(rib_file_path).split('.')[0]
    image_file_path = os.path.join(rib_file_dir, '{0}.{1}'.format(rib_file_name, DEFAULT_IMAGE_EXT))
    return image_file_path


def generate_rib_file(rib_file_path='', base_color=[1,1,0]):
    if not rib_file_path:
        rib_file_path = os.path.join(os.getcwd(), 'default.rib')
    image_file_path = get_render_image_path(rib_file_path=rib_file_path)

    ri = prman.Ri()
    rendertarget = rib_file_path
    ri.Begin(rendertarget)
    ri.Display(image_file_path, DEFAULT_IMAGE_EXT, 'rgba', {'string compression': 'pixarlog'})
    ri.Format(DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 45})
    ri.Translate(0, 0, 20)
    ri.Rotate(-90, 1, 0, 0)
    ri.WorldBegin()
    ri.Bxdf('PxrDisney', 'PxrDisney1', {'color baseColor': base_color}, 'PxrValidateBxdf')
    ri.Gemetry('teapot')
    ri.WorldEnd()
    ri.End()


def render_to_disk(rib_file_path):
    rib_file_dir = os.path.dirname(rib_file_path)
    render_log_file = os.path.join(rib_file_dir, 'render.log')
    render_cmd = 'prman -loglevel 4 -logfile {0} {1}'.format(render_log_file, rib_file_path)
    os.system(render_cmd)
    return render_log_file

def get_render_log_data(render_log_path):
    render_log = ''
    with open(render_log_path, 'r') as log_file:
        render_log = log_file.readlines()
    return render_log


if __name__ == '__main__':
    rib_file_path = '/tmp/default.rib'
    generate_rib_file(rib_file_path=rib_file_path, base_color=[1, 0, 0])
    render_log_file = render_to_disk(rib_file_path=rib_file_path)
    get_render_log_data(render_log_path=render_log_file)