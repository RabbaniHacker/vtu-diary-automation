"""
VTU Internship Diary Generator
Instantly generates a complete, formatted Word (.docx) diary for any domain
(AI/ML, Data Science, Cyber Security, Cloud, Web Dev, Python, Java)
with realistic daily tasks, learnings, blockers, and skills.

Usage:
    python generate_diary.py
"""

from datetime import date, datetime, timedelta
import os
import sys

try:
    import docx
except ImportError:
    print("[!] python-docx is required. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx>=1.1.0"])
    import docx

CURRICULA = {
    "1": {
        "name": "Artificial Intelligence & Machine Learning",
        "default_skills": ["Python", "Machine Learning", "Data Science"],
        "modules": [
            ("Orientation & Environment", "Set up Python virtual environment, installed Jupyter, NumPy, Pandas, Scikit-learn, and reviewed AI roadmap.", "Learned Python environment management and package isolation.", "Minor pip package conflict resolved with virtualenv.", ["Python", "Machine Learning", "Developer Tools"]),
            ("NumPy & Array Operations", "Practiced array creation, slicing, vectorization, linear algebra, and broadcasting with NumPy.", "Learned how vectorized operations optimize memory and execution time.", "Multi-dimensional axis operations required testing with sample matrices.", ["Python", "NumPy", "Data Analysis"]),
            ("Pandas Data Manipulation", "Loaded CSV datasets, handled missing values, applied grouping, filtering, and aggregation.", "Learned real-world data cleaning and transformation techniques.", "Handling inconsistent date and categorical columns required type conversions.", ["Pandas", "Python", "Data Cleaning"]),
            ("Data Visualization", "Built statistical plots, histograms, heatmaps, and correlation matrices using Matplotlib and Seaborn.", "Learned how visualization reveals distributions, outliers, and feature correlations.", "Adjusting subplot layouts and color maps took several iterations.", ["Data Analysis", "Python", "Visualization"]),
            ("Exploratory Data Analysis (EDA)", "Conducted comprehensive EDA on a benchmark dataset, identified skewed features, and normalized numerical columns.", "Understood how feature distributions guide model selection and preprocessing.", "Dealing with outliers required comparing IQR and Z-score methods.", ["Data Analysis", "EDA", "Machine Learning"]),
            ("Feature Engineering & Scaling", "Implemented One-Hot Encoding, Label Encoding, StandardScaler, and MinMaxScaler pipelines.", "Learned why feature scaling prevents gradient-based algorithms from diverging.", "Preventing data leakage between train and test sets required careful pipeline design.", ["Machine Learning", "Data Preprocessing", "Feature Engineering"]),
            ("Linear & Polynomial Regression", "Trained a linear regression model, evaluated Mean Squared Error, R2 score, and analyzed residuals.", "Understood regression assumptions, loss functions, and cost minimization.", "Underfitting was addressed by exploring polynomial feature expansion.", ["Machine Learning", "Regression", "Mathematics"]),
            ("Logistic Regression & Classification", "Implemented logistic regression for binary classification, computed confusion matrix, precision, recall, and ROC-AUC.", "Learned that accuracy is misleading on imbalanced datasets and how ROC-AUC reflects performance.", "Threshold tuning was needed to optimize recall.", ["Machine Learning", "Classification", "Evaluation"]),
            ("Decision Trees & Pruning", "Trained Decision Tree classifiers, visualized decision boundaries, and analyzed Gini impurity vs Entropy.", "Learned how decision trees make decisions and why unconstrained trees overfit.", "Pre-pruning using max_depth and min_samples_leaf reduced overfitting.", ["Decision Trees", "Machine Learning", "Algorithms"]),
            ("Ensemble Methods - Random Forests", "Trained Random Forest models, compared Bagging vs Boosting, and analyzed feature importances.", "Learned how ensembling reduces variance without increasing bias.", "Hyperparameter tuning increased training time on large forests.", ["Random Forest", "Ensemble Learning", "Machine Learning"]),
            ("Boosting Algorithms (XGBoost / LightGBM)", "Implemented gradient boosting, tuned learning rate, subsample ratio, and tree depth.", "Learned how sequential boosting corrects residual errors from previous estimators.", "Early stopping was implemented to prevent overfitting.", ["Machine Learning", "XGBoost", "Algorithms"]),
            ("Unsupervised Learning - K-Means & PCA", "Applied K-Means clustering, determined optimal clusters using Elbow Method, and reduced dimensions with PCA.", "Learned how dimensionality reduction preserves variance while speeding up training.", "Choosing optimal k required comparing silhouette scores.", ["Clustering", "PCA", "Machine Learning"]),
            ("Introduction to Deep Learning", "Studied perceptrons, activation functions (ReLU, Sigmoid, Softmax), forward propagation, and backpropagation.", "Understood how multi-layer neural networks learn non-linear representations.", "Mathematical derivation of gradient descent took time to trace.", ["Deep Learning", "Neural Networks", "Mathematics"]),
            ("Building Neural Networks (PyTorch/TensorFlow)", "Constructed a multi-layer feedforward network, defined loss functions, Adam optimizer, and training loop.", "Learned the mechanics of batch training, epochs, and loss convergence.", "Shape mismatches between tensor layers required debugging.", ["Deep Learning", "PyTorch", "Python"]),
            ("Convolutional Neural Networks (CNN)", "Built a CNN for image classification using Conv2D, MaxPooling, Dropout, and Flatten layers.", "Learned how convolutional filters extract spatial features from image data.", "Overfitting was mitigated using data augmentation and dropout.", ["Computer Vision", "Deep Learning", "CNN"]),
            ("Natural Language Processing (NLP)", "Practiced text tokenization, lemmatization, stop-word removal, and TF-IDF vectorization for sentiment classification.", "Learned the pipeline for converting unstructured text into numerical features.", "Handling out-of-vocabulary words and noisy characters required regex cleaning.", ["NLP", "Machine Learning", "Text Processing"]),
            ("Model Evaluation & Cross-Validation", "Implemented Stratified K-Fold cross-validation and evaluated bias-variance tradeoff across models.", "Learned how k-fold validation provides a robust estimate of generalization error.", "Long execution times for k-fold on complex ensembles required parallel jobs.", ["Model Validation", "Machine Learning", "Python"]),
            ("Model Deployment & API (FastAPI)", "Wrapped the trained model into a REST API endpoint using FastAPI and Pydantic for input validation.", "Learned how machine learning models are served in production web services.", "Handling model serialization and deserialization with Joblib required version alignment.", ["FastAPI", "API", "Python"]),
            ("Project Integration & Testing", "Integrated the ML API with a dashboard, tested edge cases with malformed payloads, and logged predictions.", "Learned end-to-end integration and the importance of input validation in production ML.", "Handling edge cases with missing input fields required fallback values.", ["Integration", "Testing", "Machine Learning"]),
            ("Final Documentation & Summary", "Documented the ML pipeline, benchmarked model metrics against baselines, and prepared final presentation.", "Consolidated practical understanding of the complete machine learning lifecycle.", "No major blockers; focused on organizing project documentation.", ["Documentation", "Machine Learning", "Presentation"])
        ]
    },
    "2": {
        "name": "Data Science & Data Analytics",
        "default_skills": ["Python", "Data Analysis", "SQL"],
        "modules": [
            ("Environment Setup & Overview", "Set up JupyterLab, Python data stack, SQL tools, and reviewed analytics lifecycle.", "Understood how analytical questions translate into structured data investigations.", "Minor path configuration issues resolved.", ["Python", "Data Analysis", "Developer Tools"]),
            ("SQL Basics & Data Extraction", "Wrote SELECT, WHERE, GROUP BY, and aggregate queries to extract business metrics.", "Learned how relational queries summarize transactional records.", "Writing efficient filters on large tables required indexing awareness.", ["SQL", "Database design", "Data Analysis"]),
            ("Advanced SQL & Joins", "Implemented INNER, LEFT, RIGHT, and FULL OUTER joins, subqueries, and window functions.", "Learned how window functions compute running totals, ranks, and moving averages.", "Null handling in outer joins required COALESCE statements.", ["SQL", "Data modeling", "Data Analysis"]),
            ("Data Cleaning with Pandas", "Identified missing values, duplicates, and inconsistent categoricals; applied imputation techniques.", "Learned standard methodologies for transforming raw dirty data into reliable datasets.", "Selecting appropriate imputation strategies for skewed variables took review.", ["Pandas", "Data Cleaning", "Python"]),
            ("Exploratory Data Analysis (EDA)", "Computed summary statistics, correlation matrices, and identified outliers across business dimensions.", "Learned how EDA uncovers anomalies, seasonality, and correlations.", "Resolving conflicting outliers required domain-specific thresholding.", ["EDA", "Data Analysis", "Python"]),
            ("Data Visualization (Matplotlib & Seaborn)", "Built bar charts, scatter plots, box plots, and heatmaps to visualize KPI distributions.", "Learned effective visual communication principles for analytical findings.", "Formatting multi-panel visualizations took several design iterations.", ["Data Analysis", "Visualization", "Python"]),
            ("Dashboarding with Power BI / Tableau", "Connected data sources, built interactive filters, KPI scorecards, and time-series drilldowns.", "Learned how interactive dashboards allow stakeholders to explore trends independently.", "Configuring table relationships and DAX measures required careful planning.", ["Power BI", "Data Analysis", "Visualization"]),
            ("Hypothesis Testing & Statistical Analysis", "Conducted t-tests, Chi-Square tests, ANOVA, and calculated p-values and confidence intervals.", "Learned how statistical significance prevents drawing false conclusions from noise.", "Interpreting p-values in multiple testing scenarios required Bonferroni corrections.", ["Statistics", "Data Analysis", "Mathematics"]),
            ("Time Series Analysis & Forecasting", "Decomposed seasonal trends, tested stationarity with ADF test, and fitted moving averages.", "Learned how time series data models trends, seasonality, and residual noise.", "Handling missing timestamps and irregular intervals required resampling.", ["Time Series", "Data Analysis", "Python"]),
            ("Documentation & Insights Presentation", "Compiled executive analytical report with actionable business recommendations and methodology.", "Learned how to translate technical metrics into executive business recommendations.", "No major blockers; finalized documentation and charts.", ["Documentation", "Data Analysis", "Presentation"])
        ]
    },
    "3": {
        "name": "Cyber Security & Ethical Hacking",
        "default_skills": ["Cyber Security", "Networking", "Linux"],
        "modules": [
            ("Security Fundamentals & Lab Setup", "Configured Kali Linux, network adapters, vulnerable test VMs, and reviewed ethics.", "Learned fundamental security concepts and legal/ethical testing boundaries.", "Configuring NAT and Host-only adapters in virtualization took troubleshooting.", ["Cyber Security", "Linux", "Virtualization"]),
            ("Networking & Protocol Analysis", "Analyzed TCP 3-way handshake, IP headers, DNS, and HTTP traffic using Wireshark.", "Understood how packet-level inspections identify malicious behavior.", "Filtering through high-volume packet captures required specific Wireshark display filters.", ["Networking", "Wireshark", "Cyber Security"]),
            ("Port Scanning & Reconnaissance", "Executed Nmap scans, service version detection, OS fingerprinting, and vulnerability scripts.", "Learned active and passive reconnaissance strategies and attack surface mapping.", "Handling firewalled ports and timing templates required adjusting scan flags.", ["Nmap", "Reconnaissance", "Cyber Security"]),
            ("Vulnerability Assessment", "Ran OpenVAS/Nessus automated scans, prioritized CVEs by CVSS scores, and filtered false positives.", "Learned the systematic approach to discovering and ranking security vulnerabilities.", "Distinguishing benign configurations from genuine risks required manual verification.", ["Vulnerability Assessment", "Cyber Security", "Audit"]),
            ("Web Application Security - OWASP Top 10", "Studied SQL Injection, Cross-Site Scripting (XSS), CSRF, and broken access controls.", "Understood how improper input validation leads to severe web vulnerabilities.", "Building test payloads on lab web applications required understanding encoding.", ["Web Security", "OWASP", "Cyber Security"]),
            ("SQL Injection & Defensive Coding", "Demonstrated SQLi bypass in lab VM, then implemented parameterized queries and input sanitization.", "Learned how prepared statements completely eliminate SQL injection vulnerabilities.", "Blind SQL injection timing payloads required careful script tracing.", ["SQL", "Security", "Web Security"]),
            ("Authentication & Cryptography", "Analyzed symmetric vs asymmetric encryption, hashing (SHA-256, bcrypt), and salt mechanisms.", "Learned why plain passwords should never be stored and how salting stops rainbow tables.", "Understanding public/private key exchanges took theoretical review.", ["Cryptography", "Security", "Cyber Security"]),
            ("Linux Security & Hardening", "Configured SSH keys, iptables/UFW firewall rules, file permissions, and disabled insecure services.", "Learned defense-in-depth principles for server infrastructure.", "Accidentally blocking SSH access during firewall rule configuration was restored via console.", ["Linux", "Server Hardening", "Security"]),
            ("Incident Response & Log Analysis", "Analyzed auth.log, syslog, and web server logs to reconstruct a simulated intrusion timeline.", "Learned how SIEM and log forensics uncover attacker footprints and lateral movement.", "Correlating log timestamps across multiple servers required synchronization checks.", ["Log Analysis", "Incident Response", "Cyber Security"]),
            ("Final Security Assessment Report", "Authored comprehensive penetration testing summary with remediation roadmap.", "Learned how to present risk impact and technical remediation to management.", "No major blockers; completed final report.", ["Documentation", "Security Audit", "Presentation"])
        ]
    },
    "4": {
        "name": "Cloud Computing & DevOps",
        "default_skills": ["Cloud Computing", "DevOps", "Docker"],
        "modules": [
            ("Cloud Fundamentals & Account Setup", "Configured cloud IAM users, MFA, budget alerts, and explored cloud service models (IaaS/PaaS).", "Learned principle of least privilege and foundational cloud architecture.", "Setting up strict IAM policies required reviewing policy JSON schemas.", ["Cloud Computing", "IAM", "Security"]),
            ("Compute & Virtual Networking", "Launched virtual instances (EC2/VM), configured VPC, subnets, route tables, and security groups.", "Learned how virtual networks isolate cloud workloads from the public internet.", "SSH connection timeout was traced to missing inbound security group rule.", ["Cloud Computing", "Networking", "DevOps"]),
            ("Cloud Storage & Database Services", "Configured object storage buckets (S3/Cloud Storage), bucket policies, and managed databases.", "Learned how cloud object storage scales with high availability and lifecycle rules.", "Public bucket access restrictions required adjusting bucket policies.", ["Cloud Computing", "Storage", "Database design"]),
            ("Linux Server Administration", "Managed systemd services, users, environment variables, bash scripting, and cron automation.", "Strengthened command-line efficiency for automated server administration.", "Debugging bash script syntax errors required running with bash -x.", ["Linux", "DevOps", "Automation"]),
            ("Docker & Containerization", "Wrote Dockerfiles, built container images, managed container lifecycles, and mapped host ports.", "Learned how containers package application dependencies for predictable execution.", "Reducing Docker image size required utilizing multi-stage builds.", ["Docker", "Containers", "DevOps"]),
            ("Multi-Container Apps (Docker Compose)", "Configured docker-compose.yml to orchestrate a web service, database, and Redis cache.", "Learned container networking and service discovery across multi-tier applications.", "Service dependency ordering required implementing healthcheck conditions.", ["Docker", "DevOps", "Microservices"]),
            ("CI/CD with GitHub Actions", "Wrote automated CI workflows for linting, testing, building Docker images, and pushing to registry.", "Learned how continuous integration catches regressions automatically on every commit.", "Fixing GitHub Actions YAML indentation and secret injection required testing.", ["DevOps", "CI/CD", "Git"]),
            ("Infrastructure as Code (Terraform)", "Wrote declarative Terraform files to provision cloud resources, state management, and variables.", "Learned how declarative IaC guarantees reproducible infrastructure environments.", "Terraform state locks and dependency order required understanding provider graph.", ["Terraform", "DevOps", "Cloud Computing"]),
            ("Cloud Monitoring & Logging", "Configured CloudWatch/Cloud Monitoring metrics, alarms, log ingestion, and alert notifications.", "Learned operational observability and how proactive alerting prevents downtime.", "Fine-tuning alert thresholds was needed to prevent notification spam.", ["Monitoring", "DevOps", "Cloud Computing"]),
            ("Project Deployment & Documentation", "Deployed containerized multi-tier app via automated pipeline and authored architecture doc.", "Consolidated practical skills in cloud architecture and automated delivery pipelines.", "No major blockers; verified public endpoint and documented architecture.", ["Documentation", "Cloud Computing", "DevOps"])
        ]
    },
    "5": {
        "name": "Python Full Stack Development",
        "default_skills": ["Python", "Web technology", "Database design"],
        "modules": [
            ("Python Core & Environment", "Set up virtual environment, reviewed data types, list comprehensions, dicts, and functions.", "Strengthened core Python foundations for application programming.", "Virtualenv activation differences across shells resolved.", ["Python", "Programming", "Developer Tools"]),
            ("OOP & Modular Architecture", "Implemented classes, inheritance, encapsulation, magic methods, and custom exceptions.", "Learned how object-oriented design structures large applications into manageable models.", "Understanding super() and multiple inheritance required tracing MRO.", ["Python", "OOP", "Clean Code"]),
            ("Database & SQL with SQLAlchemy", "Created SQLite/Postgres schemas, defined ORM models, and executed CRUD transactions.", "Learned how ORMs abstract SQL queries while preserving relational integrity.", "Managing database migrations with Alembic required checking model metadata.", ["Python", "SQL", "Database design"]),
            ("Flask / FastAPI Web APIs", "Built REST endpoints with routing, request parsing, JSON serialization, and status codes.", "Learned the request-response lifecycle in Python web frameworks.", "CORS configuration was required to allow frontend access.", ["FastAPI", "REST API", "Python"]),
            ("Authentication & Security", "Implemented JWT token authentication, password hashing with bcrypt, and route guards.", "Learned secure authentication principles and stateless token validation.", "Handling token expiration and refresh logic required middleware adjustments.", ["Authentication", "Security", "Python"]),
            ("Frontend Integration (HTML/CSS/JS)", "Built responsive frontend UI, connected API via fetch, and handled dynamic DOM updates.", "Learned how Python backends integrate with responsive client interfaces.", "Handling asynchronous state updates in the UI required defensive checks.", ["HTML", "CSS", "Java Script"]),
            ("Unit Testing & Pytest", "Wrote automated unit and integration tests using pytest, mocks, and fixtures.", "Learned how automated testing protects application contracts during refactoring.", "Mocking database connections in test fixtures required fixture scoping.", ["Software Testing", "Python", "QA"]),
            ("Deployment & Project Wrap-up", "Containerized application with Docker, configured Gunicorn server, and drafted project documentation.", "Learned the complete development to production deployment cycle for Python apps.", "No major blockers; final documentation and code review completed.", ["Deployment", "Python", "Documentation"])
        ]
    }
}


def parse_cli_date(val: str) -> date:
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y", "%d-%m-%y"):
        try:
            return datetime.strptime(val.strip(), fmt).date()
        except ValueError:
            pass
    return None


def generate_diary():
    print()
    print("=" * 60)
    print("   VTU Internship Daily Diary Generator")
    print("   Generates a complete, ready-to-use Word (.docx) file")
    print("=" * 60)
    print()
    print("Choose your Internship Domain:")
    print("  1. Artificial Intelligence & Machine Learning")
    print("  2. Data Science & Data Analytics")
    print("  3. Cyber Security & Ethical Hacking")
    print("  4. Cloud Computing & DevOps")
    print("  5. Python Full Stack Development")
    print("  6. Custom Domain (Enter your own)")
    print()

    choice = input("Enter selection (1-6) [Default: 1]: ").strip()
    if not choice:
        choice = "1"

    if choice in CURRICULA:
        curriculum_data = CURRICULA[choice]
        domain_name = curriculum_data["name"]
    else:
        domain_name = input("Enter your custom domain (e.g. Embedded Systems / Java): ").strip()
        if not domain_name:
            domain_name = "Engineering Intern"
        curriculum_data = CURRICULA["1"]

    print(f"\n[Selected Domain]: {domain_name}")

    company = input("Enter Company / Provider Name [e.g. Infosys / Internshala / Edutainer]: ").strip()
    if not company:
        company = "Internship Provider"

    start_date_str = input("Enter Start Date (DD/MM/YYYY) [Default: 03/08/2026]: ").strip()
    if start_date_str:
        start_date = parse_cli_date(start_date_str)
        if not start_date:
            print("[!] Could not parse date. Using 03/08/2026.")
            start_date = date(2026, 8, 3)
    else:
        start_date = date(2026, 8, 3)

    days_str = input("Enter Total Number of Days [Default: 110]: ").strip()
    try:
        total_days = int(days_str) if days_str else 110
    except ValueError:
        total_days = 110

    hours_str = input("Enter Daily Work Hours [Default: 5.5]: ").strip()
    if not hours_str:
        hours_str = "5.5"

    ref_link = input("Enter Reference Link [Default: https://vtu.internyet.in]: ").strip()
    if not ref_link:
        ref_link = "https://vtu.internyet.in"

    output_filename = "diary_data.docx"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)

    print()
    print(f"[*] Generating {total_days} daily diary entries...")

    doc = docx.Document()
    doc.add_heading(f"VTU Internship Daily Diary -- {company}", level=1)
    doc.add_paragraph(f"{domain_name} | {start_date.strftime('%d %b %Y')} onwards | {total_days} entries")

    modules = curriculum_data["modules"]
    num_modules = len(modules)

    current_date = start_date
    day_count = 1

    while day_count <= total_days:
        mod_idx = (day_count - 1) % num_modules
        phase_num = ((day_count - 1) // num_modules) + 1
        title, summary, learnings, blockers, skills = modules[mod_idx]

        # Add variety across cycles
        if phase_num > 1:
            work_summary = f"Phase {phase_num}: Advanced implementation - {summary}"
            outcomes = f"Phase {phase_num}: {learnings} Applied across extended project features."
        else:
            work_summary = summary
            outcomes = learnings

        heading_text = f"Day {day_count} -- {current_date.strftime('%d %B %Y')}"
        doc.add_heading(heading_text, level=2)
        doc.add_paragraph(f"Internship: {domain_name} -- {company}")
        doc.add_paragraph(f"Work Summary: {work_summary}")
        doc.add_paragraph(f"Hours Worked: {hours_str}")
        doc.add_paragraph(f"Reference Links: {ref_link}")
        doc.add_paragraph(f"Learnings / Outcomes: {outcomes}")
        doc.add_paragraph(f"Blockers / Risks: {blockers}")
        doc.add_paragraph(f"Skills Used: {', '.join(skills)}")

        day_count += 1
        current_date += timedelta(days=1)

    doc.save(output_path)
    print(f"[OK] Successfully generated: {output_filename}")
    print(f"     Total entries: {total_days}")
    print(f"     Date range   : {start_date.strftime('%d %b %Y')} -> {(current_date - timedelta(days=1)).strftime('%d %b %Y')}")
    print(f"     Hours per day: {hours_str}")
    print()
    print("Now you can simply run 'start.bat' and start your automation!")
    print()


if __name__ == "__main__":
    generate_diary()
