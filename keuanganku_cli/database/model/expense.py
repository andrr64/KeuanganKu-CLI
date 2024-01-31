from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModelExpense:
    id: int
    title: str
    time: datetime
    amount: float
    category_id: int
    rate: int 

    def __post_init__(self):
        pass
    
    def toListForInsert(self):
        '''The return must ordered same like 'expense' column order '''
        return [self.title, self.timeToStringFormat(), self.amount, self.category_id, self.rate]

    def timeToStringFormat(self) -> str:
        return datetime.strftime(self.time, "%d/%m/%y %H:%S")

    @staticmethod
    def toJson(expense):
        return {
            'id': expense.id,
            'title': expense.title,
            'time': expense.time.strftime('%Y-%m-%d %H:%M:%S'),  # Format sesuai kebutuhan Anda
            'amount': expense.amount,
            'category_id': expense.category_id,
            'rate': expense.rate
        }

    @staticmethod
    def fromTuple(tupleData):
        return ModelExpense(
            id=tupleData[0],
            title=tupleData[1],
            time=datetime.strptime(tupleData[2], "%d/%m/%y %H:%M" ),
            amount=tupleData[3],
            category_id=tupleData[4],
            rate=tupleData[5]
        )

    @staticmethod
    def fromJson(json_data):
        return ModelExpense(
            id=json_data['id'],
            title=json_data['title'],
            time=datetime.strptime(json_data['time'], '%Y-%m-%d %H:%M:%S'),  # Sesuaikan dengan format yang digunakan dalam toJson
            amount=json_data['amount'],
            category_id=json_data['category_id'],
        )
            
