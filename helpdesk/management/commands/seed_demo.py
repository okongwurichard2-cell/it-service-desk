import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from helpdesk.models import (
    Asset,
    MaintenanceRecord,
    StaffProfile,
    Ticket,
    TicketHistory,
)


class Command(BaseCommand):
    help = "Clear existing demo data and create fresh demo data."


    @transaction.atomic
    def handle(self, *args, **options):

        random.seed(20261004)

        password = "Demo@12345"


        # =========================================================
        # 1. CLEAR PREVIOUS DEMO DATA
        # =========================================================

        self.stdout.write(
            self.style.WARNING(
                "Clearing previous demo data..."
            )
        )

        # Delete helpdesk records first.
        # Related history/maintenance records are removed
        # through their foreign-key cascades.
        TicketHistory.objects.all().delete()
        Ticket.objects.all().delete()
        MaintenanceRecord.objects.all().delete()
        Asset.objects.all().delete()

        # Remove previous demo StaffProfile records.
        StaffProfile.objects.filter(
            user__username__startswith="itstaff"
        ).delete()

        StaffProfile.objects.filter(
            user__username__startswith="staff"
        ).delete()

        # Remove previous demo users.
        User.objects.filter(
            username__startswith="itstaff"
        ).delete()

        User.objects.filter(
            username__startswith="staff"
        ).delete()


        # =========================================================
        # 2. NAME DATA
        # =========================================================

        people = [
            # Igbo
            ("Chinedu", "Okafor"),
            ("Emeka", "Nwosu"),
            ("Ifeanyi", "Eze"),
            ("Nnamdi", "Obi"),
            ("Chukwuemeka", "Ugwu"),
            ("Kelechi", "Madu"),
            ("Obinna", "Anyanwu"),
            ("Uche", "Ibe"),
            ("Chiamaka", "Ezeh"),
            ("Adaeze", "Nnamani"),
            ("Ngozi", "Onyeka"),
            ("Amarachi", "Chukwu"),
            ("Ifeoma", "Okoro"),
            ("Nneka", "Madu"),
            ("Chinonso", "Ugwu"),

            # Yoruba
            ("Adewale", "Adeyemi"),
            ("Adebayo", "Olawale"),
            ("Oluwaseun", "Afolabi"),
            ("Oluwatobi", "Adebayo"),
            ("Temitope", "Adesina"),
            ("Ayodeji", "Akinyemi"),
            ("Abiola", "Ajayi"),
            ("Tunde", "Ojo"),
            ("Babatunde", "Balogun"),
            ("Femi", "Ogunleye"),
            ("Funmi", "Olawale"),
            ("Yetunde", "Adewale"),
            ("Folake", "Fashola"),
            ("Tolulope", "Oni"),
            ("Bukola", "Adebayo"),

            # Hausa / Northern
            ("Abdullahi", "Sani"),
            ("Usman", "Abubakar"),
            ("Umar", "Ibrahim"),
            ("Hassan", "Musa"),
            ("Mustapha", "Yusuf"),
            ("Bello", "Garba"),
            ("Sani", "Umar"),
            ("Abubakar", "Lawal"),
            ("Yusuf", "Mohammed"),
            ("Fatima", "Abdullahi"),
            ("Aisha", "Musa"),
            ("Zainab", "Usman"),
            ("Maryam", "Ibrahim"),
            ("Hauwa", "Sani"),

            # Other common Nigerian names
            ("Michael", "Williams"),
            ("David", "Johnson"),
            ("Daniel", "Thomas"),
            ("Samuel", "Adams"),
            ("Joshua", "Morgan"),
            ("Joseph", "Brown"),
            ("Victor", "James"),
            ("John", "Bennett"),
            ("Peter", "Cole"),
            ("Grace", "Thomas"),
            ("Deborah", "Johnson"),
            ("Esther", "Williams"),
            ("Mary", "Adams"),
            ("Blessing", "Morgan"),
            ("Sarah", "James"),
        ]


        # =========================================================
        # 3. STATIC DATA
        # =========================================================

        departments = [
            "Administration",
            "Academic Affairs",
            "Finance",
            "Human Resources",
            "Marketing",
            "Information Technology",
        ]


        ticket_titles = [
            "Computer not powering on",
            "Unable to connect to Wi-Fi",
            "Printer not responding",
            "Email account access issue",
            "System running slowly",
            "Password reset request",
            "Monitor display problem",
            "Keyboard not working",
            "Mouse stopped responding",
            "Software installation request",
            "Cannot access shared folder",
            "Network connection keeps dropping",
            "Projector not displaying",
            "Antivirus warning on workstation",
            "Browser application error",
            "Computer overheating",
            "Unable to access internal portal",
            "Printer paper jam",
            "Office network outage",
            "New workstation setup request",
        ]


        descriptions = [
            (
                "The issue started during normal working hours "
                "and prevents the user from completing the task."
            ),
            (
                "The problem occurs repeatedly and requires "
                "technical investigation."
            ),
            (
                "The user has already restarted the device "
                "but the problem persists."
            ),
            (
                "The issue is affecting normal work activities "
                "and needs technical assistance."
            ),
            (
                "The user reported the problem to the IT support "
                "desk for investigation."
            ),
        ]


        asset_names = [
            ("Dell Latitude 5420", "computer"),
            ("HP ProBook 450", "computer"),
            ("Lenovo ThinkPad E14", "computer"),
            ("Dell OptiPlex 7090", "computer"),
            ("HP LaserJet Pro M404", "printer"),
            ("Canon imageCLASS LBP6030", "printer"),
            ("TP-Link Archer C6", "network"),
            ("Cisco Catalyst 2960", "network"),
            ("Dell 24-inch Monitor", "accessory"),
            ("Logitech Wireless Keyboard", "accessory"),
            ("Logitech Wireless Mouse", "accessory"),
            ("Epson Office Projector", "other"),
        ]


        # =========================================================
        # 4. CREATE / KEEP ADMIN
        # =========================================================

        self.stdout.write(
            "Preparing admin account..."
        )

        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "System",
                "last_name": "Administrator",
                "email": "admin@aptechsys.local",
            },
        )

        if created:
            admin_user.set_password("admin321")

        admin_user.first_name = "System"
        admin_user.last_name = "Administrator"
        admin_user.email = "admin@aptechsys.local"
        admin_user.is_active = True
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()


        StaffProfile.objects.update_or_create(
            user=admin_user,
            defaults={
                "role": "it_staff",
                "department": "Information Technology",
                "phone": "08030000999",
            },
        )


        # =========================================================
        # 5. CREATE IT STAFF
        # =========================================================

        self.stdout.write(
            "Creating IT staff..."
        )

        it_staff_data = [
            ("Chinedu", "Okafor"),
            ("Adewale", "Adeyemi"),
            ("Abdullahi", "Sani"),
        ]

        it_staff = []

        for index, (first_name, last_name) in enumerate(
            it_staff_data,
            start=1,
        ):

            username = f"itstaff{index}"
            email = f"{username}@aptechsys.local"

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            user.is_active = True
            user.save()

            StaffProfile.objects.create(
                user=user,
                role="it_staff",
                department="Information Technology",
                phone=f"08030000{index:03d}",
            )

            it_staff.append(user)


        # =========================================================
        # 6. CREATE NORMAL STAFF
        # =========================================================

        self.stdout.write(
            "Creating staff users..."
        )

        staff_users = []

        selected_people = random.sample(
            people,
            20,
        )

        for index, (first_name, last_name) in enumerate(
            selected_people,
            start=1,
        ):

            username = f"staff{index:02d}"
            email = f"{username}@aptechsys.local"

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            user.is_active = True
            user.save()

            StaffProfile.objects.create(
                user=user,
                role="staff",
                department=random.choice(
                    departments[:-1]
                ),
                phone=f"0814000{index:04d}",
            )

            staff_users.append(user)


        # =========================================================
        # 7. CREATE TICKETS
        # =========================================================

        self.stdout.write(
            "Creating tickets..."
        )

        priorities = [
            "low",
            "medium",
            "medium",
            "high",
            "critical",
        ]

        statuses = [
            "open",
            "assigned",
            "in_progress",
            "resolved",
            "closed",
        ]

        tickets = []

        for index in range(1, 41):

            requester = random.choice(
                staff_users
            )

            assigned_to = random.choice(
                it_staff
            )

            status = random.choice(
                statuses
            )

            ticket = Ticket.objects.create(
                requester=requester,
                assigned_to=(
                    None
                    if status == "open"
                    else assigned_to
                ),
                title=random.choice(
                    ticket_titles
                ),
                description=random.choice(
                    descriptions
                ),
                priority=random.choice(
                    priorities
                ),
                status=status,
            )

            tickets.append(ticket)


            # Initial history
            TicketHistory.objects.create(
                ticket=ticket,
                changed_by=requester,
                old_status="",
                new_status="open",
                note="Ticket created.",
            )


            # Assignment
            if status != "open":

                TicketHistory.objects.create(
                    ticket=ticket,
                    changed_by=assigned_to,
                    old_status="open",
                    new_status="assigned",
                    note=(
                        "Ticket assigned to IT support staff."
                    ),
                )


            # In progress
            if status in {
                "in_progress",
                "resolved",
                "closed",
            }:

                TicketHistory.objects.create(
                    ticket=ticket,
                    changed_by=assigned_to,
                    old_status="assigned",
                    new_status="in_progress",
                    note=(
                        "Technical investigation started."
                    ),
                )


            # Resolved
            if status in {
                "resolved",
                "closed",
            }:

                TicketHistory.objects.create(
                    ticket=ticket,
                    changed_by=assigned_to,
                    old_status="in_progress",
                    new_status="resolved",
                    note=(
                        "Reported issue was resolved."
                    ),
                )


            # Closed
            if status == "closed":

                TicketHistory.objects.create(
                    ticket=ticket,
                    changed_by=assigned_to,
                    old_status="resolved",
                    new_status="closed",
                    note=(
                        "Ticket closed after resolution."
                    ),
                )


        # =========================================================
        # 8. CREATE ASSETS
        # =========================================================

        self.stdout.write(
            "Creating assets..."
        )

        assets = []

        asset_statuses = [
            "available",
            "available",
            "assigned",
            "maintenance",
            "retired",
        ]

        for index in range(1, 26):

            name, category = random.choice(
                asset_names
            )

            status = random.choice(
                asset_statuses
            )

            assigned_to = (
                random.choice(staff_users)
                if status == "assigned"
                else None
            )

            asset = Asset.objects.create(
                asset_tag=f"AST-{index:04d}",
                name=name,
                category=category,
                serial_number=(
                    f"SN-{random.randint(100000, 999999)}"
                ),
                status=status,
                assigned_to=assigned_to,
                purchase_date=(
                    date.today()
                    - timedelta(
                        days=random.randint(
                            30,
                            900,
                        )
                    )
                ),
                notes=(
                    "Demo asset record for the "
                    "IT service desk system."
                ),
            )

            assets.append(asset)


        # =========================================================
        # 9. CREATE MAINTENANCE RECORDS
        # =========================================================

        self.stdout.write(
            "Creating maintenance records..."
        )

        maintenance_assets = [
            asset
            for asset in assets
            if asset.status == "maintenance"
        ]

        maintenance_descriptions = [
            "Hardware inspection and troubleshooting.",
            "Routine preventive maintenance completed.",
            "Operating system and driver maintenance.",
            "Network connectivity diagnosis and repair.",
        ]

        for asset in maintenance_assets:

            MaintenanceRecord.objects.create(
                asset=asset,
                performed_by=random.choice(
                    it_staff
                ),
                description=random.choice(
                    maintenance_descriptions
                ),
                cost=random.choice([
                    0,
                    2500,
                    5000,
                    7500,
                    10000,
                ]),
                maintenance_date=(
                    timezone.localdate()
                    - timedelta(
                        days=random.randint(
                            1,
                            90,
                        )
                    )
                ),
            )


        # =========================================================
        # 10. SUMMARY
        # =========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Demo data reset and created successfully."
            )
        )

        self.stdout.write("")
        self.stdout.write(
            "LOGIN CREDENTIALS"
        )

        self.stdout.write(
            "Admin: admin / admin321"
        )

        self.stdout.write(
            "IT Staff: itstaff1 / Demo@12345"
        )

        self.stdout.write(
            "Staff: staff01 / Demo@12345"
        )

        self.stdout.write("")

        self.stdout.write(
            "RECORD COUNTS"
        )

        self.stdout.write(
            f"IT Staff: {len(it_staff)}"
        )

        self.stdout.write(
            f"Staff: {len(staff_users)}"
        )

        self.stdout.write(
            f"Tickets: {Ticket.objects.count()}"
        )

        self.stdout.write(
            f"Ticket History: {TicketHistory.objects.count()}"
        )

        self.stdout.write(
            f"Assets: {Asset.objects.count()}"
        )

        self.stdout.write(
            f"Maintenance Records: "
            f"{MaintenanceRecord.objects.count()}"
        )