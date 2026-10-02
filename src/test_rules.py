from analytics import get_category_mom, get_reseller_activity
from rules import find_category_alerts, find_inactive_resellers

category_df = get_category_mom()
reseller_df = get_reseller_activity()

category_alerts = find_category_alerts(category_df)
inactive_alerts = find_inactive_resellers(reseller_df)

print("Category alerts:")
print()

for alert in category_alerts:
    print(alert)

print()
print("Inactive reseller alerts:")
print()

for alert in inactive_alerts:
    print(alert)