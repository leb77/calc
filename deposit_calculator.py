#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой калькулятор для расчёта дохода по банковскому вкладу
с использованием формулы сложных процентов
"""

def calculate_deposit_growth(initial_amount, annual_rate, years):
    """
    Рассчитывает рост вклада по формуле сложных процентов
    
    Args:
        initial_amount (float): Начальная сумма вклада
        annual_rate (float): Годовая процентная ставка (в процентах)
        years (int): Количество лет
    
    Returns:
        list: Список кортежей (год, сумма_на_начало, проценты, сумма_на_конец)
    """
    results = []
    current_amount = initial_amount
    
    for year in range(1, years + 1):
        # Рассчитываем проценты за год
        interest = current_amount * (annual_rate / 100)
        # Новая сумма в конце года
        end_amount = current_amount + interest
        
        # Сохраняем результаты для текущего года
        results.append((year, current_amount, interest, end_amount))
        
        # Обновляем сумму для следующего года (формула сложных процентов)
        current_amount = end_amount
    
    return results

def print_deposit_table(results):
    """
    Выводит таблицу с результатами расчёта вклада
    
    Args:
        results (list): Результаты расчёта вклада
    """
    print("Расчёт роста вклада по годам:")
    print("-" * 70)
    print(f"{'Год':<5} | {'Сумма на начало':<15} | {'Проценты':<12} | {'Сумма на конец':<15}")
    print("-" * 70)
    
    for year, start_amount, interest, end_amount in results:
        print(f"{year:<5} | {start_amount:<15,.2f} | {interest:<12,.2f} | {end_amount:<15,.2f}")
    
    print("-" * 70)

def main():
    """
    Основная функция программы
    """
    print("Калькулятор дохода по банковскому вкладу")
    print("=" * 50)
    
    # Начальные параметры
    initial_amount = 3_000_000  # 3 миллиона рублей
    annual_rate = 19  # 19% годовых
    years = 5  # Количество лет (от 1 до 5)
    
    print(f"Начальная сумма вклада: {initial_amount:,} руб.")
    print(f"Годовая процентная ставка: {annual_rate}%")
    print(f"Расчёт на {years} лет(года)")
    print()
    
    # Рассчитываем рост вклада
    results = calculate_deposit_growth(initial_amount, annual_rate, years)
    
    # Выводим таблицу
    print_deposit_table(results)
    
    # Выводим дополнительную информацию
    total_income = results[-1][3] - initial_amount
    print(f"\nИтоговый доход за {years} лет: {total_income:,.2f} руб.")
    print(f"Конечная сумма: {results[-1][3]:,.2f} руб.")

if __name__ == "__main__":
    main()