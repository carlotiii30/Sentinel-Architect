import os
from architect import SentinelArchitect
from colorama import Fore, Style, init

init(autoreset=True)


def run_architect_demo():
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "🏗️  SENTINEL-ARCHITECT: SECURE IaC GENERATOR")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

    architect = SentinelArchitect()

    user_request = (
        "Create a Docker Compose environment for a Python Web App and a PostgreSQL DB. "
        "The DB must be in a private network, and all secrets must use environment variables. "
        "Apply hardening to the containers."
    )

    print(f"\n📝 {Fore.YELLOW}User Request: {Fore.WHITE}{user_request}")
    print(f"{Fore.BLUE}🚀 Generating secure architecture and files...\n")

    try:
        result = architect.generate_infrastructure(user_request)

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"{Fore.YELLOW}📂 Generating Infrastructure Files:")
        for file in result.files:
            file_path = os.path.join(output_dir, file.filename)
            with open(file_path, "w") as f:
                f.write(file.content)
            print(f"{Fore.GREEN}  ✅ Created: {Fore.WHITE}{file_path}")

        checklist_path = os.path.join(output_dir, "VALIDATION.md")
        with open(checklist_path, "w") as f:
            f.write("# 🛡️ Security Validation Checklist\n\n")
            f.write(
                "Follow these steps to verify the security of the generated infrastructure:\n\n"
            )
            for item in result.validation_checklist:
                f.write(f"- [ ] {item}\n")

        print(f"{Fore.GREEN}  ✅ Created: {Fore.WHITE}{checklist_path}")

    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")

    print(Fore.CYAN + Style.BRIGHT + "\n✅ Infrastructure Design Completed.")


if __name__ == "__main__":
    run_architect_demo()
