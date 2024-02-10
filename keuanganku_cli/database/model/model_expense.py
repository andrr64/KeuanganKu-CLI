from dataclasses import dataclass
from datetime import datetime
from database.model.model_expense_category import ModelExpenseCategory

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
    def timeToStringFormatSimple(self) -> str:
        return datetime.strftime(self.time, "%d/%m/%y")

    @property
    def timeToUnix(self) -> int:
        return int(self.time.timestamp())

    @staticmethod
    def fromTuple(tupleData, expenseCategory : ModelExpenseCategory):
        return ModelExpense(
            id=tupleData[0],
            title=tupleData[1],
            time=datetime.utcfromtimestamp(tupleData[2]),
            amount=tupleData[3],
            category= expenseCategory,
            category_id=expenseCategory.id,
            rate=tupleData[5]
        )

    @staticmethod
    def printTableColumn() -> str:
        return f"{'Title':<10} | {'Amount':<15} | {'Category':<20} | Time"

    def __str__(self) -> str:
        amount = f'{self.amount:,.2f}'
        categoryTitle = ''
        if len(self.category.title) > 20:
            categoryTitle = self.category.title[0:17] + '...'
        else:
            categoryTitle = f'{self.category.title:<20}'
        title = f"{self.title:<10}" if len(self.title)  < 10 else f"{self.title[0:7]}..."
        return f"{title} | {amount:>15} | {categoryTitle} | {self.timeToStringFormat}"