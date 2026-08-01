import os

def find_file(project_path, filename):
    for root, dirs, files in os.walk(project_path):
        if filename in files:
            return True
    return False


def find_directory(project_path, dirname):
    for root, dirs, files in os.walk(project_path):
        if dirname in dirs:
            return True
    return False


def analyze_project(project_path):

    report = {

    "score": score,

    "language": language,

    "tools":{

        "docker":True,
        "docker_compose":True,
        "terraform":False,
        "kubernetes":True,
        "jenkins":False,
        "github_actions":False,
        "readme":True

    },

    "checks":[...],

    "recommendations":[...]

}

    score = 0

    # --------------------
    # Docker
    # --------------------

    if find_file(project_path, "Dockerfile"):
        report["checks"].append("✅ Dockerfile found")
        score += 10
    else:
        report["checks"].append("❌ Dockerfile missing")
        report["recommendations"].append(
            "Create a Dockerfile to containerize your application."
        )

    # --------------------
    # Docker Compose
    # --------------------

    if find_file(project_path, "docker-compose.yml"):
        report["checks"].append("✅ docker-compose.yml found")
        score += 10
    else:
        report["checks"].append("❌ docker-compose.yml missing")

    # --------------------
    # Terraform
    # --------------------

    if find_directory(project_path, "terraform"):
        report["checks"].append("✅ Terraform folder found")
        score += 10
    else:
        report["recommendations"].append(
            "Infrastructure as Code using Terraform is recommended."
        )

    # --------------------
    # Kubernetes
    # --------------------

    if find_directory(project_path, "k8s") or find_directory(project_path, "kubernetes"):
        report["checks"].append("✅ Kubernetes manifests found")
        score += 10
    else:
        report["recommendations"].append(
            "Consider adding Kubernetes deployment manifests."
        )

    # --------------------
    # GitHub Actions
    # --------------------

    if find_directory(project_path, ".github"):
        report["checks"].append("✅ GitHub Actions workflow found")
        score += 10

    # --------------------
    # Jenkins
    # --------------------

    if find_file(project_path, "Jenkinsfile"):
        report["checks"].append("✅ Jenkins Pipeline found")
        score += 10

    # --------------------
    # Language Detection
    # --------------------

    if find_file(project_path, "requirements.txt"):
        report["language"] = "Python"
        score += 10

    elif find_file(project_path, "package.json"):
        report["language"] = "Node.js"
        score += 10

    elif find_file(project_path, "pom.xml"):
        report["language"] = "Java"
        score += 10

    # --------------------
    # README
    # --------------------

    if find_file(project_path, "README.md"):
        report["checks"].append("✅ README found")
        score += 10
    else:
        report["recommendations"].append(
            "Add a README.md for documentation."
        )

    # --------------------
    # Final Score
    # --------------------

    report["score"] = score

    return report
