from jinja2 import Environment, FileSystemLoader
import json
import click


@click.command()
@click.argument("base_path")
@click.argument("template_name")
@click.argument("output")
@click.option("--data", default="{}", help="template data JSON")
def render_templates(base_path, template_name, output, data):
    fs_loader = FileSystemLoader(base_path)
    env = Environment(loader=fs_loader)
    template = env.get_template(template_name)
    template_data = json.loads(data)
    if output == "-":
        print template.render(template_data)
    else:
        with open(output, "w") as fp:
            fp.write(template.render(template_data))


if __name__ == "__main__":
    render_templates()
