import os

from virtualenv import create_environment

def main():
    #create_environment(home_dir, site_packages=True, clear=False,
    # unzip_setuptools=False, use_distribute=False, prompt=None,
    # search_dirs=None, never_download=False)

    vpath = r'/tmp/test'

    create_environment(vpath, site_packages=False)
    os.chdir(vpath)
    os.system(r'%s/bin/pip install requests' % vpath)


if __name__ == '__main__':
    main()
