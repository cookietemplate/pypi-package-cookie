import nox


{%- if cookiecutter.use_pytest == 'y' %}
@nox.session
def tests(session):
    session.install('poetry')
    session.run('poetry', 'install')
    session.run('poetry', 'run', 'pytest', '--cov={{cookiecutter.project_slug}}', '--cov-report=term-missing', '--cov-report=html')
    session.notify('coverage')


{%- endif %}
{%- if cookiecutter.use_coverage == 'y' %}
@nox.session
def coverage(session):
    session.install('coverage')
    session.run('coverage', 'report', '--show-missing', '--fail-under={{cookiecutter.coverage_threshold}}')
    session.run('coverage', 'erase')


{%- endif %}
{%- if cookiecutter.use_lint == 'y' %}
@nox.session
def lint(session):
    session.install('toml', 'yapf', 'flake8', 'pyproject-flake8')
    session.run('yapf', '--in-place', '--recursive', './{{cookiecutter.project_slug}}')
    session.run('flake8', '{{cookiecutter.project_slug}}')


{%- endif %}
{%- if cookiecutter.use_pdoc == 'y' %}
@nox.session
def build_docs(session):
    session.install('poetry', 'pdoc')
    session.run('poetry', 'install')
    session.run('poetry', 'run', 'pdoc', '--output-dir', 'docs', '-d', 'google', '{{cookiecutter.project_slug}}')
{%- endif %}
