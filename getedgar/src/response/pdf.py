from subprocess import call
import os


def create_pdf(url, name):
    try:
        path = os.getcwd().replace("spiders", "out")
        call(["wkhtmltopdf", url, '{0}/{1}.pdf'.format(path,name)])
    except:
        print("ERROR ---- NO SE CREA EL PDF: NO SE ENCUENTRA INSTALADO LA APLICACION wkhtmltopdf")