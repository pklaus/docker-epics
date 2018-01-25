#!/usr/bin/env python

# Via http://pydanny.com/jinja2-quick-load-function.html
from jinja2 import FileSystemLoader, Environment

from build_configuration import BUILDS

def render_from_template(directory, template_name, **kwargs):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template-file', '-f', metavar='Dockerfile.jinja2', default='Dockerfile.jinja2', help='The Dockerfile template to use.')
    subparsers = parser.add_subparsers(dest='action')
    parser_render = subparsers.add_parser('render', help='Render the template')
    parser_build =  subparsers.add_parser('build',  help='Render the template and build the image')
    for template_parser in parser_render, parser_build:
        template_parser.add_argument('--tag', choices=BUILDS.keys(), required=True, help='The tag to build (implies the base image to derive from).')
    args = parser.parse_args()
    kwargs = BUILDS[args.tag]
    content = render_from_template('.', args.template_file, **kwargs)
    with open('Dockerfile', 'w') as f:
        f.write(content)
    if 'build' in args.action:
        import os
        os.system(f'docker build -t {args.tag} .')

if __name__ == "__main__": main()
