# System Design: Redwood Constellation

## Concept

An immersive 3D web experience simulating a redwood forest. Users navigate this virtual space where falling "leaves" represent senior citizens. Each leaf emits a short audio quote when nearby. Clicking a leaf allows the user to listen to the senior's full life story. The goal is to create a repository of wisdom and experience, accessed through an engaging visual metaphor.

## System Architecture
```ascii
+---------------------+      +---------------------+      +-----------------------+
|     User Browser    |<---->|    Web Server/CDN   |<---->|      Load Balancer    |
| (Frontend: 3D       |      | (Static Assets: JS, |      |                       |
|  Forest, React/Vue, |      |  CSS, Models,       |      +-----------+-----------+
|  Three.js, Web      |      |  Textures)          |                  |
|  Audio API)         |      +---------------------+                  |
+----------+----------+                                                |
           |                                                           V
           | API Requests (Fetch stories, quotes)           +-----------+-----------+
           |                                                |    Backend API Server |
           V                                                |  (Node/Python/etc.)   |
+----------+----------+      +-------------------------+    |  - Story/Quote Meta   |
|   Audio Storage     |<-----| Audio Processing Pipeline |<---|  - User Interaction   |
| (Cloud Storage/CDN) |      | (Python/Librosa/FFmpeg) |    |                       |
| - Full Stories      |      | - Normalize, Transcode  |    +-----------+-----------+
| - Short Quotes      |      | - Quote Extraction      |                | DB Queries
+---------------------+      | - Metadata Generation   |                V
                           +-------------------------+      +-----------+-----------+
                                          ^                 |       Database        |
                                          | Upload          |    (PostgreSQL/Mongo) |
                           +--------------+--------------+  |  - Story Metadata     |
                           | Senior/Admin Upload Portal |  |  - Quote Metadata     |
                           | (Separate Interface)       |  |  - (Optional) Users   |
                           +----------------------------+  +-----------------------+
```

**Components:**

1.  **User Browser (Frontend):**
    *   Renders the 3D forest using `Three.js` or similar.
    *   Manages user navigation (first-person controls).
    *   Handles interaction (detecting proximity to leaves, clicks).
    *   Uses the Web Audio API for spatialized quote playback and streaming full stories.
    *   UI framework (React, Vue, Svelte) manages state and components.
2.  **Web Server/CDN:**
    *   Serves the static frontend assets (HTML, CSS, JavaScript bundles).
    *   Crucially, serves the 3D models, textures, and potentially the short audio quotes via a CDN for low latency.
3.  **Load Balancer:**
    *   Distributes incoming API requests across multiple backend server instances for scalability and reliability.
4.  **Backend API Server:**
    *   Built with Node.js/Express, Python/Flask/Django, etc.
    *   Provides endpoints to fetch leaf/story metadata based on user location or interaction.
    *   Handles fetching data from the database.
    *   (Optional) Manages user authentication and profiles.
5.  **Database:**
    *   Stores metadata about each story/senior (ID, name, quote text, URLs to audio files, potential positional hints).
    *   (Optional) Stores user data.
6.  **Audio Storage (Cloud):**
    *   Stores the actual audio files (short quotes, full stories) using services like AWS S3 or Google Cloud Storage.
    *   Ideally integrated with the CDN for efficient delivery.
7.  **Audio Processing Pipeline:**
    *   An offline or backend process (potentially using Python scripts like your `process_audio.py`).
    *   Takes raw recordings uploaded by seniors/admins.
    *   Normalizes volume, transcodes to web-friendly formats (Opus, AAC).
    *   Automates the extraction of short audio quotes.
    *   Generates necessary metadata and uploads processed files to Audio Storage and updates the Database.
8.  **Senior/Admin Upload Portal:**
    *   A separate, simpler web interface (or potentially a script-based workflow).
    *   Allows authorized users to upload raw audio recordings and associated information (senior's name, etc.).
    *   Triggers the Audio Processing Pipeline.

## Project Plan (1-3 Months - MVP Focus)

This assumes a small, focused team (e.g., 1-2 developers) aiming for a Minimum Viable Product (MVP).

**Month 1: Core Experience & Foundation**

*   **Goal:** Build the basic interactive 3D forest and core audio playback.
*   **Tasks:**
    *   Set up project structure (Frontend framework, 3D library).
    *   Implement basic 3D scene: terrain, lighting, simple tree representation.
    *   Implement first-person navigation controls.
    *   Create a basic "leaf" representation (e.g., sprite or simple geometry).
    *   Implement proximity detection for leaves.
    *   Implement Web Audio API playback for:
        *   A *single* hardcoded short quote on proximity.
        *   A *single* hardcoded full story on click.
    *   Set up basic backend API structure (e.g., Flask/Node) with a placeholder endpoint.
    *   Set up Git repository and basic development environment.
*   **Deliverable:** A functional local prototype demonstrating core navigation, leaf interaction, and audio playback with sample assets.

**Month 2: Data Integration & Backend Development**

*   **Goal:** Connect the frontend to a dynamic backend, manage real story data.
*   **Tasks:**
    *   Design database schema for stories/quotes.
    *   Implement backend API endpoints to:
        *   Fetch nearby leaf data (quote URL, metadata).
        *   Fetch full story data (URL, metadata) on click.
    *   Connect frontend to fetch data from the API instead of using hardcoded values.
    *   Implement dynamic leaf generation/placement based on backend data.
    *   Set up cloud storage (S3/GCS) for audio files.
    *   Develop initial version of the Audio Processing Pipeline (manual trigger is okay for MVP):
        *   Basic normalization and transcoding.
        *   Manual quote extraction (or simple automated split).
    *   Manually upload a small set (5-10) of processed stories and quotes.
*   **Deliverable:** Frontend dynamically loads and plays audio/data served from the backend API and cloud storage. Basic audio processing script exists.

**Month 3: Polish, Optimization & Basic Deployment**

*   **Goal:** Optimize performance, refine visuals, implement the upload mechanism, and prepare for initial deployment.
*   **Tasks:**
    *   Optimize 3D assets (LODs, texture compression).
    *   Implement frontend optimizations (instancing for leaves, lazy loading).
    *   Refine visual aesthetics (better lighting, simple atmospheric effects).
    *   Develop the basic Senior/Admin Upload Portal (simple web form).
    *   Integrate Upload Portal with the Audio Processing Pipeline.
    *   Set up basic cloud infrastructure (e.g., simple EC2/App Engine instance, RDS/Cloud SQL database, CDN).
    *   Implement basic monitoring and logging.
    *   Testing (manual walkthroughs, basic API tests).
    *   Prepare deployment scripts/CI basics.
*   **Deliverable:** An MVP version deployed to a staging/simple production environment. Seniors/admins can upload new stories via the portal. Basic performance optimizations implemented.

## Cost Estimation (Highly Variable)

Charging for a project like this depends heavily on scope, team location/experience, specific features, ongoing maintenance, and content creation effort. This is a **very rough estimate** for the 1-3 month MVP described above, assuming a small freelance team or agency in a Western market.

*   **Development Labor (1-2 Developers, 3 Months):** $30,000 - $90,000+
    *   This is the largest component. Rates vary wildly ($50-$150+/hr per developer).
*   **Infrastructure Costs (Monthly, Post-MVP):** $50 - $300+ / month
    *   Cloud hosting (compute, database, storage, CDN bandwidth). Scales with usage. Starts low, can grow significantly with high traffic/storage.
*   **Content Creation/Curation:** Variable
    *   Are you providing the senior stories/recordings, or does that need to be budgeted separately (interviews, editing)? This can be a significant hidden cost.
*   **Software/Licenses:** ~$0 - $100 / month
    *   Mostly open-source, but some tools or specific 3D assets might have costs.
*   **Contingency (15-20%):** $5,000 - $18,000+

**Total MVP Estimate:** **$35,000 - $110,000+**

**Factors Influencing Cost:**

*   **Complexity of 3D visuals:** Highly realistic forests are much more expensive than stylized ones.
*   **Number of initial stories:** More content means more processing and storage.
*   **Advanced features:** User accounts, search, complex spatial audio, VR support would add significant cost.
*   **Scalability requirements:** Designing for massive traffic upfront increases complexity and cost.
*   **Team location and structure:** Offshore teams might be cheaper in labor but add communication overhead.

**Recommendation:** Start with a clearly defined MVP scope (like the 3-month plan) to control initial costs and validate the core concept before investing in more advanced features.

## DevOps Pipeline for Seniors

The "Senior/Admin Upload Portal" and "Audio Processing Pipeline" form the basis of this. A robust DevOps approach would involve:

1.  **Automated Upload:** The portal triggers the processing pipeline automatically upon successful upload.
2.  **Pipeline Automation:** The pipeline steps (validation, normalization, transcoding, quote extraction, metadata generation, storage upload, database update) are fully scripted and automated.
3.  **Status Tracking:** The portal provides feedback to the uploader on the processing status (e.g., "Processing," "Complete," "Error").
4.  **Error Handling:** Robust error handling and logging within the pipeline. Notifications for failures.
5.  **Infrastructure as Code (IaC):** Define the pipeline infrastructure (e.g., serverless functions, container definitions) using tools like Terraform or CloudFormation for reproducible deployments.
6.  **CI/CD for the Pipeline:** The pipeline code itself should be under version control and have automated tests and deployment.

This ensures a reliable, scalable, and low-friction way for seniors or administrators to contribute stories to the Redwood Constellation.