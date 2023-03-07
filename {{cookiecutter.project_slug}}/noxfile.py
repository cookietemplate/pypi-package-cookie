import nox


{%- if cookiecutter.use_pytest == 'y' %}
@nox.session
def tests(session):
    session.install('pytest', 'pytest-cov', 'poetry')
    session.run('poetry', 'install')
    session.run('pytest', '--cov=package_name', '--cov-report=term-missing', '--cov-report=html')
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
    session.install('pdoc')
    session.run('pdoc', '--html', '--output-dir', 'docs', '-d', 'google', '{{cookiecutter.project_slug}}')
{%- endif %}
