import csv

from os import listdir, makedirs
from os.path import isfile, join, exists

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

import model

SYMBOLS_TO_IGNORE = ["SPAXX**", "CORE**", "NHX700908"]

if __name__ == '__main__':

    if not exists("output"):
        makedirs("output")

    engine = create_engine('sqlite:///output/Fidelity.db')

    model.Base.metadata.bind = engine
    model.Base.metadata.create_all()

    session = sessionmaker(bind=engine)()

    directory = "/Users/andrewfinke/Documents/Fidelity/output/"
    for f in [f for f in listdir(directory) if isfile(join(directory, f))]:
        path = join(directory, f)

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)

            date_string = path.split("_")[-1].strip('.csv')
            datetime_object = datetime.strptime(date_string, '%b-%d-%Y')

            print(datetime_object)

            for row in reader:
                account_name = row["Account Name/Number"]
                symbol = row["Symbol"]

                if len(account_name) > 15:
                    continue
                elif symbol in SYMBOLS_TO_IGNORE:
                    continue

                entry = model.SymbolEODEntry(datetime_object, row)

                try:
                    session.add(entry)
                    session.commit()
                except Exception as e:
                    session.rollback()
