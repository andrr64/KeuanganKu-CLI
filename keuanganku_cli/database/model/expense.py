from dataclasses import dataclass
from datetime import datetime
from database.model.expense_category import ModelExpenseCategory

@dataclass
class ModelExpense:
    id: int
    title: str
    time: datetime
    amount: float
    category_id : int
    category : ModelExpenseCategory
    rate: int 

    def __post_init__(self):
        pass
    
    def toListForInsert(self):
        '''The return must ordered same like 'expense' column order '''
        return [self.title, self.timeToUnix, self.amount, self.category.id, self.rate]

    @property
    def timeToStringFormat(self) -> str:
        return datetime.strftime(self.time, "%d/%m/%y %H:%S")
    
    @property
    def timeToUnix(self) -> int:
        return int(self.time.timestamp())

    @staticmethod
    def fromTuple(tupleData, expenseCategory : ModelExpenseCategory):
        return ModelExpense(
            id=tupleData[0],
            title=tupleData[1],
            time=datetime.strptime(tupleData[2], "%d/%m/%y %H:%M" ),
            amount=tupleData[3],
            category= expenseCategory,
            category_id=expenseCategory.id,
            rate=tupleData[5]
        )

    def __str__(self) -> str:
        amount = f'{self.amount:,.0f}'
        categoryTitle = f'{self.category.title:<20}'
        title = f"{self.title:<10}" if len(self.title)  < 10 else f"{self.title[0:7]}..."
        return f"{title} | {amount} | {categoryTitle} | {self.timeToStringFormat}"