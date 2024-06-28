from setuptools import setup, find_packages

setup(
    name='html-tag-modifier',  # Nom de votre application ou module
    version='1.0',              # Version de votre application ou module
    py_modules=['modifier_html'],  # Nom du module principal sans l'extension .py
    install_requires=[
        'beautifulsoup4',  # Dépendances requises pour votre script
    ],
    entry_points={
        'console_scripts': [
            'modifier-html = modifier_html:main',  # Remplacez 'modifier_html:main' par le nom de votre fichier et la fonction principale à exécuter
        ],
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
