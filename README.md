# Voice Biometric Service

## Project Overview
This service uses a Makefile to simplify build, run, and test operations.

## Documents:
Project Schema: Confluence[https://vinbdi-slp.atlassian.net/wiki/spaces/VB2P/pages/1814660454/Project+Management?force_transition=7ec89756-27e9-4205-a84f-d739a912cad7]

### 1. **Install**  
   ```bash
   make install
   ```

### 2. **Run**  
   ```bash
   make run
   ```

### 3. **Format**  
   ```bash
   make format
   ```

### 4. **Test**  
   ```bash
   make test
   ```

### 5. **Generate Migrations**  
   ```bash
   DESCRIPTION=<DESCRIPTION> make generate_migration
   ```

### 6. **Install Pre-commit hook**  
   ```bash
   make install_precommit
   ```