import os


class SaveFile:

    @staticmethod
    def write_in_doc(url,name,description,company,cik,sic,filing,date_doc, file_name):
        path = os.getcwd().replace("spiders", "out")
        file = open('{0}\{1}.csv'.format(path, str(file_name)), 'a')
        register = "\n{0},{1},{2},{3},{4},{5},{6}".format(
            str(sic),
            company.replace(',', ''),
            str(cik),
            str(url),
            str(filing),
            description.replace(',', ''),
            str(date_doc)
        )
        file.write(register)
        file.close()