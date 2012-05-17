#!/usr/bin/env python
from django_pancake.flatten import flatten, TemplateDirectory
import os

def template_names(input_dir, prefix=''):
    for filename in os.listdir(input_dir):
        template_name = os.path.join(prefix, filename)
        full_name = os.path.join(input_dir, filename)
        if os.path.isdir(full_name) and filename != "admin":
            for name in template_names(full_name, template_name):
                yield name
        else:
            yield template_name

def make_pancakes(input_dir, output_dir):
    templates = TemplateDirectory(input_dir)
    for template_name in template_names(input_dir):
        if template_name == "admin":
            continue
        print "Writing %s" % template_name
        pancake = flatten(template_name, templates)
        outfile = os.path.join(output_dir, template_name)
        try:
            os.makedirs(os.path.dirname(outfile))
        except OSError: # Already exists.
            pass
        with open(outfile, 'w') as fp:
            fp.write(pancake)

if __name__ == "__main__":
    import sys
    if len(sys.argv[1:]) != 2:
        print >> sys.stderr, 'Usage: %s source_dir target_dir' % sys.argv[0]
        raise SystemExit(1)
    make_pancakes(sys.argv[1], sys.argv[2])
