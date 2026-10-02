from analytics import (
    get_category_metrics,
    get_reseller_activity,
    get_region_metrics,
    get_category_mom,
)


print("\nCategory metrics")
print(get_category_metrics())

print("\nReseller activity")
print(get_reseller_activity())

print("\nRegion metrics")
print(get_region_metrics())

print("\nCategory month-over-month")
print(get_category_mom())