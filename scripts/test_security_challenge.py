"""
Security Challenge & Adversarial Stress Testing Harness
Milestone 1 & 2 Verification Suite

Tests gitignore rules, adversarial edge cases, vital file preservation,
and scans the repository for credential leaks or exposed secrets.
Uses dynamic environment secret loading and generic pattern matching
to prevent hardcoding any live credentials or project references in repository files.
"""

import os
import sys
import subprocess
import zipfile
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_local_env_secrets():
    """
    Dynamically loads secrets and project references from the untracked local .env file (if present)
    without hardcoding any credentials in repository scripts.
    Returns:
        tuple[list[str], list[bytes]]: (string_secrets, byte_secrets)
    """
    string_secrets = set()
    env_path = REPO_ROOT / ".env"
    if env_path.is_file():
        try:
            content = env_path.read_text(encoding="utf-8", errors="ignore")
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if not v:
                    continue
                # If value is a connection URL (e.g. postgresql://user:pass@host:port/db)
                url_match = re.search(r"://([^:]+):([^@]+)@", v)
                if url_match:
                    user_part, pwd_part = url_match.group(1), url_match.group(2)
                    if pwd_part and pwd_part not in ["your-password", "your-database-password", "<PASSWORD>", "[YOUR-PASSWORD]"]:
                        string_secrets.add(pwd_part)
                    if "." in user_part:
                        # e.g., postgres.<project_ref> -> project ref
                        ref_part = user_part.split(".", 1)[1]
                        if ref_part and ref_part not in ["your-project-ref", "<PROJECT_REF>", "[YOUR-PROJECT-REF]"]:
                            string_secrets.add(ref_part)
                elif k.upper() in ["SUPABASE_PASSWORD", "SUPABASE_PROJECT_REF", "DATABASE_PASSWORD", "DB_PASSWORD"]:
                    if v not in ["your-password", "your-database-password", "your-project-ref"]:
                        string_secrets.add(v)
        except Exception:
            pass

    byte_secrets = [s.encode("utf-8") for s in string_secrets if s]
    return list(string_secrets), byte_secrets


class ChallengeRunner:
    def __init__(self):
        self.results = []
        self.failures = []
        self.env_string_secrets, self.env_byte_secrets = load_local_env_secrets()

    def log(self, category: str, test_name: str, passed: bool, detail: str = ""):
        self.results.append({
            "category": category,
            "test_name": test_name,
            "passed": passed,
            "detail": detail
        })
        status_symbol = "PASS" if passed else "FAIL"
        print(f"[{status_symbol}] [{category}] {test_name}: {detail}")
        if not passed:
            self.failures.append((category, test_name, detail))

    def run_git_check_ignore(self, path_str: str) -> bool:
        """Returns True if git check-ignore indicates the path is ignored."""
        cmd = ["git", "check-ignore", "-q", path_str]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0

    def test_standard_exclusions(self):
        """Suite 1: Standard sensitive patterns from .gitignore"""
        standard_targets = [
            (".env", True),
            ("docs/gcp_service_account.json", True),
            ("venv/", True),
            (".venv/", True),
            ("env/", True),
            ("ENV/", True),
            (".pytest_cache/", True),
            (".ipynb_checkpoints/", True),
            ("notebooks/.ipynb_checkpoints/", True),
            ("notebooks/.ipynb_checkpoints/01_eda_and_cleaning-checkpoint.ipynb", True),
            (".agents/", True),
            ("__pycache__/", True),
            ("scripts/__pycache__/test.cpython-313.pyc", True),
            (".vscode/", True),
            (".idea/", True),
            ("Thumbs.db", True),
            (".DS_Store", True)
        ]
        for target, should_ignore in standard_targets:
            is_ignored = self.run_git_check_ignore(target)
            passed = (is_ignored == should_ignore)
            detail = f"Expected ignored={should_ignore}, got ignored={is_ignored}"
            self.log("Standard Exclusions", f"Target: {target}", passed, detail)

    def test_adversarial_patterns(self):
        """Suite 2: Adversarial edge cases and dummy secret files"""
        adversarial_targets = [
            # Nested .env variants
            ("subfolder/.env", True),
            ("scripts/.env", True),
            ("nested/dir/.env.local", True),
            ("frontend/.env.production", True),
            ("temp_secret.env", True),
            # Key & Certificate variants
            ("server.key", True),
            ("nested/ssl/server.key", True),
            ("cert.pem", True),
            ("docs/cert.pem", True),
            ("backup.p12", True),
            ("keys/app.pfx", True),
            ("root.pkcs12", True),
            # Service account & credentials patterns
            ("test_service_account.json", True),
            ("my_service_account_prod.json", True),
            ("oauth_credentials.json", True),
            ("docs/test.json", True),
            ("docs/gcp_credentials.json", True),
            ("credentials/secret.txt", True),
            ("secrets/api_keys.yml", True),
            # Explicit un-ignore exception
            (".env.example", False)
        ]
        for target, should_ignore in adversarial_targets:
            is_ignored = self.run_git_check_ignore(target)
            passed = (is_ignored == should_ignore)
            detail = f"Expected ignored={should_ignore}, got ignored={is_ignored}"
            self.log("Adversarial Patterns", f"Target: {target}", passed, detail)

    def test_vital_files_preservation(self):
        """Suite 3: Ensure essential project files are NOT ignored"""
        vital_files = [
            "Olist_Dashboard.pbix",
            "README.md",
            "PROJECT.md",
            "PROJECT_EXECUTION_LOG.md",
            "requirements.txt",
            ".env.example",
            "reports/olist_executive_dashboard.pdf",
            "reports/executive_presentation.pptx",
            "reports/findings_report.md",
            "reports/system_integrity_audit_report.md",
            "docs/data_dictionary.md",
            "docs/setup_guide.md",
            "docs/assets/dashboard_executive_overview.png",
            "docs/assets/dashboard_sales_deep_dive.png",
            "docs/assets/dashboard_logistics_sentiment.png",
            "notebooks/01_eda_and_cleaning.ipynb",
            "output/data_quality_report.md",
            "Data Set/olist_orders_dataset.csv",
            "Data Set/olist_customers_dataset.csv",
            "Data Set/olist_order_items_dataset.csv",
            "output/star_schema/fact_orders.csv",
            "output/star_schema/dim_customers.csv",
            "scripts/etl_pipeline.py",
            "scripts/generate_presentation.py",
            "scripts/generate_pro_presentation.py",
            "scripts/load_bigquery.py",
            "scripts/load_supabase.py",
            "scripts/simulate_new_orders.py",
            "scripts/system_integrity_audit.py",
            "scripts/update_and_run_notebook.py"
        ]
        for vf in vital_files:
            file_path = REPO_ROOT / vf
            exists = file_path.exists()
            is_ignored = self.run_git_check_ignore(vf)
            passed = exists and (not is_ignored)
            detail = f"Exists on disk={exists}, Ignored={is_ignored}"
            self.log("Vital Files Preservation", f"File: {vf}", passed, detail)

    def test_live_filesystem_dummy_stress(self):
        """Suite 4: Physically create dummy test secret files, verify git ignores them, then remove them"""
        dummy_files = [
            ("temp_secret.env", "SECRET=12345"),
            ("test_service_account.json", '{"type": "service_account"}'),
            ("docs/test_dummy_secret.json", '{"private_key": "dummy"}'),
            ("ssl_test.key", "-----BEGIN " + "PRIVATE KEY-----\ntest\n-----END " + "PRIVATE KEY-----"),
            ("cert_test.pem", "-----BEGIN " + "CERTIFICATE-----\ntest\n-----END " + "CERTIFICATE-----"),
            ("credentials/dummy.json", '{"secret": true}'),
            ("secrets/keys.txt", "token=12345")
        ]
        for rel_path, content in dummy_files:
            p = REPO_ROOT / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            try:
                p.write_text(content, encoding="utf-8")
                # Check with git status -s
                status_res = subprocess.run(["git", "status", "--porcelain", str(rel_path)],
                                            cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # If ignored, porcelain status output will be empty
                tracked_or_untracked = status_res.stdout.strip()
                is_ignored = self.run_git_check_ignore(rel_path)
                passed = is_ignored and (tracked_or_untracked == "")
                detail = f"Created on disk, ignored={is_ignored}, status='{tracked_or_untracked}'"
                self.log("Filesystem Stress Test", f"Dummy: {rel_path}", passed, detail)
            finally:
                if p.exists():
                    p.unlink()
                # Clean up empty parent dir if we created credentials/ or secrets/
                if p.parent != REPO_ROOT and not any(p.parent.iterdir()):
                    try:
                        p.parent.rmdir()
                    except Exception:
                        pass

    def test_repository_credential_leak_scan(self):
        """Suite 5: Scan all non-ignored project text files for credentials and private keys"""
        known_bad_strings = [
            "-----BEGIN " + "RSA PRIVATE KEY-----",
            "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
            "-----BEGIN " + "EC PRIVATE KEY-----",
            "-----BEGIN " + "PRIVATE KEY-----"
        ]
        # Append dynamic live secrets from untracked .env (if present)
        known_bad_strings.extend(self.env_string_secrets)

        # Get list of tracked files from git ls-files
        tracked_res = subprocess.run(["git", "ls-files"],
                                     cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        files_to_scan = [f.strip() for f in tracked_res.stdout.splitlines() if f.strip()]

        # Add any untracked or modified files from git status (excluding ignored)
        status_res = subprocess.run(["git", "status", "-uall", "--porcelain"],
                                    cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in status_res.stdout.splitlines():
            line = line.strip()
            if line:
                parts = line.split(maxsplit=1)
                if len(parts) == 2 and parts[1] not in files_to_scan:
                    files_to_scan.append(parts[1])

        scanned_count = 0
        leaks_found = []

        for rel_file in files_to_scan:
            # Skip test scanner script itself
            if "test_security_challenge" in rel_file:
                continue
            full_path = REPO_ROOT / rel_file
            if not full_path.is_file():
                continue
            # Skip large binary files
            if full_path.suffix.lower() in [".pbix", ".pdf", ".pptx", ".png", ".jpg", ".zip", ".pyc"]:
                continue
            # Skip large datasets
            if full_path.stat().st_size > 5 * 1024 * 1024:
                continue

            scanned_count += 1
            try:
                text = full_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            for bad_str in known_bad_strings:
                if bad_str in text:
                    leaks_found.append((rel_file, f"Prohibited pattern/secret match: {bad_str[:3]}..."))

            # Regex for Google service account JSON private key
            if '"private_key":' in text and '"type": "service_account"' in text:
                leaks_found.append((rel_file, 'service_account private_key block'))

            # Regex for hardcoded passwords in URLs
            for match in re.finditer(r'postgresql(?:\+\w+)?://([^:]+):([^@]+)@', text):
                user, pwd = match.group(1), match.group(2)
                if pwd not in ['<PASSWORD>', 'your-password', '[YOUR-PASSWORD]', 'your-database-password']:
                    leaks_found.append((rel_file, f"Database password exposed: {user}:***"))

        passed = len(leaks_found) == 0
        detail = f"Scanned {scanned_count} files. Found {len(leaks_found)} leaks: {leaks_found}"
        self.log("Secret Leak Scan", "Repository Trackable Files Scan", passed, detail)

    def test_env_example_sanitization(self):
        """Suite 6: Verify .env.example contains zero live secrets and only placeholders"""
        env_ex_path = REPO_ROOT / ".env.example"
        if not env_ex_path.exists():
            self.log("Env Example Audit", ".env.example exists", False, "File missing")
            return

        text = env_ex_path.read_text(encoding="utf-8")
        
        # Check standard placeholders exist
        has_placeholder_pwd = "your-password" in text or "your-database-password" in text
        has_placeholder_ref = "your-project-ref" in text

        # Verify zero dynamic live secrets from untracked .env appear in .env.example
        dynamic_leaks = [s for s in self.env_string_secrets if s in text]

        # Generic check: verify no unredacted postgresql credential URI with non-placeholder user/pass
        raw_uri_leak = False
        for match in re.finditer(r'postgresql(?:\+\w+)?://([^:]+):([^@]+)@', text):
            user, pwd = match.group(1), match.group(2)
            if pwd not in ['<PASSWORD>', 'your-password', '[YOUR-PASSWORD]', 'your-database-password']:
                raw_uri_leak = True
            if user not in ['postgres.your-project-ref', 'postgres.<PROJECT_REF>', 'postgres.[YOUR-PROJECT-REF]']:
                raw_uri_leak = True

        passed = has_placeholder_pwd and has_placeholder_ref and (len(dynamic_leaks) == 0) and (not raw_uri_leak)
        detail = f"Placeholders={has_placeholder_pwd and has_placeholder_ref}, Dynamic leaks={len(dynamic_leaks)}, Raw URI leak={raw_uri_leak}"
        self.log("Env Example Audit", ".env.example Sanitization", passed, detail)

    def test_pbix_model_inspection(self):
        """Suite 7: Inspect Olist_Dashboard.pbix internal archive streams"""
        pbix_path = REPO_ROOT / "Olist_Dashboard.pbix"
        if not pbix_path.exists():
            self.log("PBIX Inspection", "Olist_Dashboard.pbix exists", False, "File missing")
            return

        passed = True
        findings = []
        pem_header = b"-----BEGIN " + b"PRIVATE KEY-----"

        with zipfile.ZipFile(pbix_path, "r") as z:
            for item in z.infolist():
                content = z.read(item.filename)
                # Check for dynamic secrets from local untracked .env
                for sec_bytes in self.env_byte_secrets:
                    if sec_bytes and sec_bytes in content:
                        passed = False
                        findings.append(f"Secret match in {item.filename}")
                # Check for PEM private key
                if pem_header in content:
                    passed = False
                    findings.append(f"Private key in {item.filename}")

        detail = f"Inspected {len(z.namelist())} internal zip streams. Findings: {findings if findings else 'Clean - Zero embedded secrets'}"
        self.log("PBIX Inspection", "Embedded Credentials Audit", passed, detail)

    def run_all(self):
        print("=" * 80)
        print("RUNNING ADVERSARIAL SECURITY & EXCLUSION CHALLENGE SUITE")
        print("=" * 80)
        self.test_standard_exclusions()
        self.test_adversarial_patterns()
        self.test_vital_files_preservation()
        self.test_live_filesystem_dummy_stress()
        self.test_repository_credential_leak_scan()
        self.test_env_example_sanitization()
        self.test_pbix_model_inspection()
        print("=" * 80)
        total = len(self.results)
        failed = len(self.failures)
        passed = total - failed
        print(f"SUMMARY: {passed}/{total} Passed, {failed} Failed.")
        print("=" * 80)
        return failed == 0

if __name__ == "__main__":
    runner = ChallengeRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
