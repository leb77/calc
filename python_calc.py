import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Исходные данные
initial_investment = 3_000_000  # первоначальный капитал
deposit_rate = 0.19              # процент по депозиту
mortgage_rate = 0.06             # ипотечная ставка
rent_initial = 40_000            # стартовая аренда
rent_growth_rate = 0.08          # темп роста аренды
property_price = 8_000_000       # первоначальная стоимость недвижимости
down_payment = 3_000_000         # первоначальный взнос
loan_amount = 5_000_000          # сумма кредита
mortgage_term = 10 * 12          # срок кредита в месяцах
inflation_rate = 0.07            # уровень инфляции
property_growth_rate = 0.08      # темп роста цен на недвижимость
tax_benefit_rate = 0.13          # налоговая льгота по ипотеке
investment_horizon = 10           # горизонт планирования (лет)

# Базовые вычисления
def compound_interest(P, r, t):
    return P * (1 + r) ** t

def mortgage_payment(P, r, n):
    mthly_rate = r / 12
    payment = P * (mthly_rate * (1 + mthly_rate)**n) / ((1 + mthly_rate)**n - 1)
    return payment

# Графики и финансовые показатели
def simulate_investment(deposit_rate=deposit_rate, mortgage_rate=mortgage_rate, rent_growth_rate=rent_growth_rate):
    deposit_balance = []
    rental_income = []
    mortgage_expenses = []
    equity = []
    break_even_point = None
    
    for year in range(1, investment_horizon + 1):
        # Депозит
        balance_deposits = compound_interest(initial_investment, deposit_rate, year)
        
        # Недвижимость
        # Изменение стоимости недвижимости
        property_value = property_price * (1 + property_growth_rate) ** year
        
        # Доход от аренды
        monthly_rent = rent_initial * (1 + rent_growth_rate) ** year
        yearly_rental_income = monthly_rent * 12
        
        # Платежи по ипотеке
        monthly_mortgage_payment = mortgage_payment(loan_amount, mortgage_rate, mortgage_term)
        yearly_mortgage_payment = monthly_mortgage_payment * 12
        
        # Налоговый вычет
        tax_benefit = yearly_mortgage_payment * tax_benefit_rate
        
        # Остаточная задолженность по ипотеке
        remaining_loan = max(loan_amount - monthly_mortgage_payment * min(year * 12, mortgage_term), 0)
        
        # Капитализация собственности
        equity_in_property = down_payment + (property_value - remaining_loan)
        
        # Финансовые потоки по инвестициям
        cash_flow_real_estate = yearly_rental_income - yearly_mortgage_payment + tax_benefit
        
        # Анализируем точку безубыточности
        if not break_even_point and balance_deposits >= equity_in_property:
            break_even_point = year
            
        deposit_balance.append(balance_deposits)
        rental_income.append(cash_flow_real_estate)
        mortgage_expenses.append(yearly_mortgage_payment)
        equity.append(equity_in_property)
    
    return {
        'deposit': deposit_balance,
        'equity': equity,
        'break_even_point': break_even_point
    }

# Анализ чувствительности
def sensitivity_analysis():
    rates = np.linspace(0.05, 0.25, num=10)  # Диапазон ставок от 5% до 25%
    results = {}
    
    for rate in rates:
        result = simulate_investment(deposit_rate=rate)
        results[rate] = result['break_even_point']
    
    return results

# Строим графики
def plot_results(results):
    fig, ax = plt.subplots(figsize=(10, 6))
    years = list(range(1, len(results['deposit']) + 1))
    
    # ГРАФИК №1: Рост капитала
    ax.plot(years, results['deposit'], label='Депозит')
    ax.plot(years, results['equity'], label='Недвижимость', linestyle='--')
    ax.set_title('Рост капитала по двум инвестиционным сценариям')
    ax.set_xlabel('Годы')
    ax.set_ylabel('Капитал (руб.)')
    ax.legend()
    plt.grid(True)
    plt.savefig('capital_growth.png')  # Сохраняем график
    plt.show()

# Анализ чувствительности и точка безубыточности
results = simulate_investment()
sensitivity_data = sensitivity_analysis()

# График анализа чувствительности
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(sensitivity_data.keys(), sensitivity_data.values())
ax.set_title('Зависимость точки безубыточности от ставки депозита')
ax.set_xlabel('Ставка депозита (%)')
ax.set_ylabel('Срок достижения безубыточности (годы)')
plt.grid(axis='y')
plt.savefig('sensitivity_analysis.png')  # Сохраняем график
plt.show()

# Результаты моделирования
plot_results(results)

# Точка безубыточности
if results['break_even_point']:
    print(f"Точка безубыточности достигнута через {results['break_even_point']} лет.")
else:
    print("Безубыточность не достигается за указанный период.")

# Итоговые рекомендации
if results['break_even_point'] is not None and results['break_even_point'] < 5:
    recommendation = "Рекомендуется выбрать покупку недвижимости."
elif results['break_even_point'] > 5 or results['break_even_point'] is None:
    recommendation = "Рекомендуется размещение средств на депозите."
else:
    recommendation = "Необходимо провести дополнительный анализ рисков."

print(f'Итоговая рекомендация: {recommendation}')

# Сохранение результатов
with open('investment_report.txt', 'w') as file:
    file.write(f'Точка безубыточности: {results["break_even_point"]}\n')
    file.write(f'Итоговая рекомендация: {recommendation}\n')
