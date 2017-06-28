class QueryResults():
    @staticmethod
    def get_task(subject,type,last_date,task):
        type = "Текущее" if type == 'C' else "Модульное"
        return "Предмет: " + subject+"\n"+"Тип: "+ type +"\n"+"Срок: "+last_date+"\n"+"Задание: "+task+"\n\n\n"