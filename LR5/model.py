from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class CurrencyRate(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    cur = Column(String(3), nullable=False)  # Код валюты (USD, EUR и т.д.)
    date = Column(DateTime, default=datetime.now)  # Дата обновления
    value = Column(Float)  # Значение курса


class CurrencyRatesCRUD:
    def __init__(self, currency_rates_obj):
        # Инициализация SQLAlchemy
        self.engine = create_engine('sqlite:///data.sqlite3')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.__currency_rates_obj = currency_rates_obj

    def create(self, data=None):
        session = self.Session()
        try:
            if data is None:
                data = self.__currency_rates_obj.values

            if not data:
                print("Нет данных для записи")
                return False

            # Очищаем старые данные
            session.query(CurrencyRate).delete()

            # Добавляем новые
            for item in data:
                rate = CurrencyRate(
                    cur=item[0],
                    date=datetime.strptime(item[1], '%d-%m-%Y %H:%M'),
                    value=float(item[2]))
                session.add(rate)

                session.commit()
                print(f"Успешно записано {len(data)} записей")
            return True
        except Exception as e:
            session.rollback()
            print(f"Ошибка при записи в БД: {e}")
            return False
        finally:
            session.close()

    def read(self, char_code=None):
        session = self.Session()
        try:
            query = session.query(CurrencyRate)
            if char_code:
                query = query.filter(CurrencyRate.cur == char_code)

            results = query.order_by(CurrencyRate.date.desc()).all()
            return [(r.cur, r.date.strftime('%d-%m-%Y %H:%M'), r.value) for r in results]
        except Exception as e:
            print(f"Ошибка при чтении из БД: {e}")
            return []
        finally:
            session.close()

    def update(self, new_data):
        return self.create(new_data)

    def delete(self, currency_code=None):
        session = self.Session()
        try:
            query = session.query(CurrencyRate)
            if currency_code:
                query = query.filter(CurrencyRate.cur == currency_code)

            deleted_count = query.delete()
            session.commit()
            return deleted_count
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении: {e}")
            return 0
        finally:
            session.close()