from datetime import datetime

address_data = [
    {
        "address_id": 1,
        "address_line_1": "6826 Herzog Via",
        "address_line_2": None,
        "district": "Avon",
        "city": "New Patienceburgh",
        "postal_code": "28441",
        "country": "Turkey",
        "phone": "1803 637401",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "address_id": 2,
        "address_line_1": "179 Alexie Cliffs",
        "address_line_2": None,
        "district": None,
        "city": "Aliso Viejo",
        "postal_code": "99305-7380",
        "country": "San Marino",
        "phone": "9621 880720",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "address_id": 3,
        "address_line_1": "148 Sincere Fort",
        "address_line_2": None,
        "district": None,
        "city": "Lake Charles",
        "postal_code": "89360",
        "country": "Samoa",
        "phone": "0730 783349",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
]

counter_party_data = [
    {
        "counterparty_id": 1,
        "counterparty_legal_name": "Fahey and Sons",
        "legal_address_id": 1,
        "commercial_contact": "Micheal Toy",
        "delivery_contact": "Mrs. Lucy Runolfsdottir",
        "created_at": datetime.fromtimestamp(1667485251.563),
        "last_updated": datetime.fromtimestamp(1667485251.563),
    },
    {
        "counterparty_id": 2,
        "counterparty_legal_name": "Leannon, Predovic and Morar",
        "legal_address_id": 2,
        "commercial_contact": "Melba Sanford",
        "delivery_contact": "Jean Hane III",
        "created_at": datetime.fromtimestamp(1667485251.563),
        "last_updated": datetime.fromtimestamp(1667485251.563),
    },
    {
        "counterparty_id": 3,
        "counterparty_legal_name": "Armstrong Inc",
        "legal_address_id": 3,
        "commercial_contact": "Jane Wiza",
        "delivery_contact": "Myra Kovacek",
        "created_at": datetime.fromtimestamp(1667485251.563),
        "last_updated": datetime.fromtimestamp(1667485251.563),
    },
]

currency_data = [
    {
        "currency_id": 1,
        "currency_code": "GBP",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "currency_id": 2,
        "currency_code": "USD",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "currency_id": 3,
        "currency_code": "EUR",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
]

department_data = [
    {
        "department_id": 1,
        "department_name": "Sales",
        "location": "Manchester",
        "manager": "Richard Roma",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "department_id": 2,
        "department_name": "Purchasing",
        "location": "Manchester",
        "manager": "Naomi Lapaglia",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "department_id": 3,
        "department_name": "Production",
        "location": "Leeds",
        "manager": "Chester Ming",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
]

staff_data = [
    {
        "staff_id": 1,
        "first_name": "Jeremie",
        "last_name": "Franey",
        "department_id": 1,
        "email_address": "jeremie.franey@terrifictotes.com",
        "created_at": datetime.fromtimestamp(1667485251.563),
        "last_updated": datetime.fromtimestamp(1667485251.563),
    },
    {
        "staff_id": 2,
        "first_name": "Deron",
        "last_name": "Beier",
        "department_id": 2,
        "email_address": "deron.beier@terrifictotes.com",
        "created_at": datetime.fromtimestamp(1667485251.563),
        "last_updated": datetime.fromtimestamp(1667485251.563),
    },
    {
        "staff_id": 3,
        "first_name": "Jeanette",
        "last_name": "Erdman",
        "department_id": 3,
        "email_address": "jeanette.erdman@terrifictotes.com",
        "created_at": datetime.fromtimestamp(1667485251.563),
        "last_updated": datetime.fromtimestamp(1667485251.563),
    },
]

design_data = [
    {
        "design_id": 1,
        "created_at": datetime.fromtimestamp(1667485249.962),
        "design_name": "Wooden",
        "file_location": "/usr",
        "file_name": "wooden-20220717-npgz.json",
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "design_id": 2,
        "created_at": datetime.fromtimestamp(1673549409.935),
        "design_name": "Bronze",
        "file_location": "/private",
        "file_name": "bronze-20221024-4dds.json",
        "last_updated": datetime.fromtimestamp(1673549409.935),
    },
    {
        "design_id": 3,
        "created_at": datetime.fromtimestamp(1675791070.093),
        "design_name": "Bronze",
        "file_location": "/lost+found",
        "file_name": "bronze-20230102-r904.json",
        "last_updated": datetime.fromtimestamp(1675791070.093),
    },
]

payment_type_data = [
    {
        "payment_type_id": 1,
        "payment_type_name": "SALES_RECEIPT",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "payment_type_id": 2,
        "payment_type_name": "SALES_REFUND",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
    {
        "payment_type_id": 3,
        "payment_type_name": "PURCHASE_PAYMENT",
        "created_at": datetime.fromtimestamp(1667485249.962),
        "last_updated": datetime.fromtimestamp(1667485249.962),
    },
]

sales_order_data = [
    {
        "sales_order_id": 1,
        "created_at": datetime.fromtimestamp(1667485252.186),
        "last_updated": datetime.fromtimestamp(1667485252.186),
        "design_id": 1,
        "staff_id": 1,
        "counterparty_id": 1,
        "units_sold": 42972,
        "unit_price": 3.94,
        "currency_id": 1,
        "agreed_delivery_date": "2022-11-07",
        "agreed_payment_date": "2022-11-08",
        "agreed_delivery_location_id": 1,
    },
    {
        "sales_order_id": 2,
        "created_at": datetime.fromtimestamp(1667485252.188),
        "last_updated": datetime.fromtimestamp(1667485252.188),
        "design_id": 2,
        "staff_id": 2,
        "counterparty_id": 2,
        "units_sold": 65839,
        "unit_price": 2.91,
        "currency_id": 2,
        "agreed_delivery_date": "2022-11-06",
        "agreed_payment_date": "2022-11-07",
        "agreed_delivery_location_id": 2,
    },
    {
        "sales_order_id": 3,
        "created_at": datetime.fromtimestamp(1667485252.188),
        "last_updated": datetime.fromtimestamp(1667485252.188),
        "design_id": 3,
        "staff_id": 3,
        "counterparty_id": 3,
        "units_sold": 32069,
        "unit_price": 3.89,
        "currency_id": 3,
        "agreed_delivery_date": "2022-11-05",
        "agreed_payment_date": "2022-11-07",
        "agreed_delivery_location_id": 3,
    },
]

totesys_seed_data = [
    {"table_name": "address", "seed_data": address_data},
    {
        "table_name": "counterparty",
        "seed_data": counter_party_data,
    },
    {"table_name": "currency", "seed_data": currency_data},
    {"table_name": "department", "seed_data": department_data},
    {"table_name": "staff", "seed_data": staff_data},
    {"table_name": "design", "seed_data": design_data},
    {"table_name": "payment_type", "seed_data": payment_type_data},
    {"table_name": "sales_order", "seed_data": sales_order_data},
]
