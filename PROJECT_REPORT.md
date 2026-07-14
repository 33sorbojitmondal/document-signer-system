# DIGITAL SIGNATURE SYSTEM

## A Full-Stack Web Application for Secure Document Authentication

---

**A Project Report**

Submitted in partial fulfillment of the requirements for the degree of

**Bachelor of Technology**

in

**Computer Science & Engineering**

---

**Submitted By:**

RAHUL PANJA (18700122011)

SK SAHIL AKTAR (18700122093)

---

**Under the Guidance of:**

Prof. Argha Kusum Das

---

**Department of Computer Science & Engineering**

**Techno International New Town**

**MAKAUT — CS781 Project II (Final Year)**

**July 2026**

---

\newpage

## CERTIFICATE

This is to certify that the project report entitled **"Digital Signature System"** submitted by **RAHUL PANJA (18700122011)** and **SK SAHIL AKTAR (18700122093)** in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering is a record of bonafide work carried out by them under my supervision and guidance.

The matter embodied in this report has not been submitted earlier for the award of any degree or diploma to the best of my knowledge.

---

**Prof. Argha Kusum Das**

Project Guide

Department of Computer Science & Engineering

Techno International New Town

---

\newpage

## ABSTRACT

The rapid digitization of business processes has created an urgent need for secure mechanisms to authenticate and verify digital documents. Traditional paper-based document signing is inherently inefficient, time-consuming, and incompatible with modern digital workflows. Furthermore, digital documents transmitted over networks are vulnerable to forgery, tampering, and unauthorized modifications, raising significant legal and security concerns regarding document authenticity.

This project presents the design and implementation of a Document Signer System, an enterprise-grade secure digital signature solution built as a full-stack web application. The system employs RSA-2048 cryptographic algorithms with SHA-256 hashing to generate mathematically verifiable digital signatures that guarantee document authenticity, integrity, and non-repudiation. The application follows a layered Model-View-Controller architecture using Python and the Django web framework for the backend, SQLite for secure data persistence, and a modern dark-themed web interface for user interaction.

The system provides comprehensive functionality including user registration with automatic cryptographic key pair generation, secure document upload and storage, digital signature creation using the signer's private key, and real-time signature verification with tamper detection capabilities. Experimental results demonstrate that the system successfully detects unauthorized document modifications and validates authentic signatures with complete accuracy. This project establishes a practical foundation for secure digital document processing and contributes to addressing real-world challenges of document forgery in digital environments.

**Keywords:** Digital Signature, RSA Cryptography, Document Authentication, Tamper Detection, Django, SHA-256, Data Integrity

---

\newpage

## TABLE OF CONTENTS

| Chapter | Title | Page |
|---------|-------|------|
| 1 | Introduction | |
| 2 | Literature Survey and Background | |
| 3 | System Analysis | |
| 4 | System Requirements | |
| 5 | System Design | |
| 6 | Implementation | |
| 7 | Testing and Results | |
| 8 | Conclusion and Future Scope | |
| | References | |

---

\newpage

## CHAPTER 1: INTRODUCTION

### 1.1 Background

In the contemporary digital era, organizations across all sectors are transitioning from paper-based documentation to electronic document management systems. This transformation, while offering substantial improvements in efficiency, accessibility, and cost reduction, introduces new categories of security challenges that were not present in traditional physical document workflows. When a document exists purely in digital form, it becomes trivially easy for malicious actors to create unauthorized copies, alter content without visible traces, or impersonate legitimate signatories. These vulnerabilities undermine the fundamental trust that document signing is intended to establish.

Digital signatures emerged as the cryptographic solution to this problem, providing a mathematical framework through which the authenticity and integrity of electronic documents can be verified with the same level of confidence as handwritten signatures on physical paper. A digital signature binds the identity of a signer to the specific content of a document at a particular point in time, creating a permanent and verifiable record that cannot be repudiated by the signer and cannot be forged by third parties.

### 1.2 Problem Statement

Despite the theoretical maturity of digital signature technology, practical implementations remain fragmented and inaccessible for many organizations. Traditional paper-based document signing continues to dominate in sectors where legal validity and audit trails are paramount, primarily because existing digital solutions are either prohibitively expensive, require specialized hardware, or lack user-friendly interfaces that non-technical personnel can operate confidently. Additionally, many current systems fail to provide transparent tamper detection mechanisms, leaving users unable to independently verify whether a received document has been modified after signing.

The absence of standardized, accessible digital signature mechanisms in current systems creates a significant gap between the security capabilities that modern cryptography offers and the tools actually available to end users. This gap represents both a security risk for organizations handling sensitive documents and a barrier to the complete digitization of administrative and legal workflows.

### 1.3 Objectives

The primary objective of this project is to design and implement a secure, user-friendly digital signature system that democratizes access to cryptographic document authentication. Specifically, the project aims to develop RSA-2048 and ECDSA-based digital signature mechanisms that provide mathematically provable document authentication, implement robust tamper detection that identifies unauthorized modifications to signed documents, create an intuitive web-based platform that enables users without cryptographic expertise to sign and verify documents, and establish a secure database architecture for storing user credentials, document metadata, and cryptographic signature records.

### 1.4 Scope

The scope of this project encompasses the complete software development lifecycle from requirements analysis through deployment-ready implementation. The system handles user registration and authentication, document upload in common file formats, digital signature generation and storage, signature verification with tamper detection, and a web-based dashboard for document management. The project does not extend to legal compliance certification, hardware security module integration, or multi-party signing workflows, which are identified as directions for future development.

---

\newpage

## CHAPTER 2: LITERATURE SURVEY AND BACKGROUND

### 2.1 Digital Signatures in Cryptography

The concept of digital signatures was first formally proposed by Diffie and Hellman in 1976 as an application of public-key cryptography. Unlike symmetric encryption systems that use a single shared key for both encryption and decryption, public-key cryptography employs mathematically related key pairs wherein information encrypted with one key can only be decrypted with the corresponding partner key. Digital signatures exploit this asymmetry by using the private key to create a signature that can only be verified using the associated public key, thereby proving that the signature was created by the holder of the private key.

The security of digital signatures rests on the computational infeasibility of deriving a private key from its corresponding public key, a property guaranteed by the mathematical hardness of problems such as integer factorization in RSA and the elliptic curve discrete logarithm problem in ECDSA. Modern digital signature schemes also incorporate cryptographic hash functions to handle documents of arbitrary size, producing a fixed-length digest that is then signed rather than signing the entire document directly.

### 2.2 RSA Algorithm

The RSA algorithm, developed by Rivest, Shamir, and Adleman in 1977, remains one of the most widely deployed public-key cryptosystems. Its security derives from the difficulty of factoring the product of two large prime numbers. In the context of digital signatures, RSA with Probabilistic Signature Scheme padding and SHA-256 hashing provides a robust combination that is recommended by current cryptographic standards including NIST SP 800-57 and PKCS #1 v2.2.

For this project, RSA-2048 was selected as the key size, providing approximately 112 bits of security strength which is considered adequate for most commercial and governmental applications through the year 2030. The signing process computes a SHA-256 hash of the document content and then applies the RSA private key operation with PSS padding to produce the final signature. Verification reverses this process using the public key and compares the recovered hash against a freshly computed hash of the received document.

### 2.3 Related Work

Several commercial digital signature platforms exist in the market, including DocuSign, Adobe Sign, and HelloSign, which provide cloud-based signing services with legal compliance features. Academic research has explored various enhancements including blockchain-based signature verification, biometric-augmented signing, and threshold signature schemes for distributed signing authority. However, these solutions typically require subscription fees, internet connectivity for verification, and trust in third-party certificate authorities. The present project addresses the educational and small-scale organizational need for a self-contained, transparent, and comprehensible digital signature implementation.

---

\newpage

## CHAPTER 3: SYSTEM ANALYSIS

### 3.1 Existing System

The conventional approach to document authentication relies on physical signatures applied to paper documents, often accompanied by notarization or witness attestation for legal weight. In partially digitized environments, organizations may scan signed paper documents into PDF format, apply simple electronic signatures that are essentially images overlaid on documents, or use password-protected files as a rudimentary access control measure. None of these approaches provide cryptographic proof of document integrity or signer identity.

Simple electronic signatures, which include scanned signature images, typed names, or checkbox confirmations, offer no protection against document tampering because the signature itself is merely a visual element that can be copied, moved, or applied to different documents. Password protection prevents unauthorized access but does not detect whether the document content has been altered by someone who possesses the password. These limitations make existing informal digital signing practices unsuitable for documents where authenticity and integrity are legally or operationally critical.

### 3.2 Proposed System

The proposed Document Signer System replaces these inadequate mechanisms with a cryptographically sound signing and verification pipeline accessible through a standard web browser. Upon registration, each user receives a unique RSA-2048 key pair generated by the system and stored securely in the database. When a user uploads a document and requests signing, the system computes a SHA-256 hash of the file content and signs this hash with the user's private key using RSA-PSS padding. The resulting signature, along with the document hash and metadata, is stored in the database and associated with the document record.

Verification allows any authorized user to confirm that a document's current content matches the content that was signed. The system recomputes the SHA-256 hash of the current file, verifies the stored signature against this hash using the signer's public key, and compares the computed hash with the hash recorded at signing time. Any discrepancy indicates either an invalid signature or post-signing tampering, both of which are reported clearly to the user through the web interface.

### 3.3 Feasibility Study

The proposed system is technically feasible using well-established open-source libraries and frameworks. The Python cryptography library provides production-grade implementations of RSA key generation, signing, and verification. The Django web framework offers mature support for user authentication, file upload handling, database ORM, and template rendering. The computational requirements are modest, as RSA-2048 operations complete in milliseconds on standard hardware, and the storage requirements scale linearly with the number of users and documents. Economic feasibility is high because all components are open-source and deployable on standard server infrastructure without licensing costs.

---

\newpage

## CHAPTER 4: SYSTEM REQUIREMENTS

### 4.1 Hardware Requirements

The Document Signer System is designed to operate on standard computing hardware without specialized cryptographic processors or hardware security modules. The development and testing environment requires a personal computer with an Intel Core i5 processor or equivalent, a minimum of 8 gigabytes of RAM, at least 500 megabytes of available storage for the application, database, and uploaded documents, and a network interface for browser-based access. These specifications are readily available in modern laptop and desktop computers used in academic and professional settings.

### 4.2 Software Requirements

The software stack for this project consists entirely of open-source components that are freely available and well-documented. The operating system supported for development is Microsoft Windows 10 or 11, though the application is cross-platform and can be deployed on Linux servers. Python version 3.10 or higher serves as the primary programming language for implementing the cryptographic logic, business rules, and server-side processing. The Django web framework version 4.2 provides the application structure, URL routing, authentication system, and database abstraction layer.

The cryptography library version 43.0 provides the RSA key generation, signing, and verification functions that form the security core of the application. SQLite serves as the embedded database engine for development and demonstration purposes, storing user accounts, document metadata, cryptographic keys, and signature records. The frontend is built with HTML5, CSS3, and Bootstrap 5 for responsive layout, with custom styling to achieve the dark-themed professional interface shown in the system screenshots. Visual Studio Code is used as the integrated development environment, and a modern web browser such as Google Chrome or Mozilla Firefox is used for testing and accessing the application interface.

### 4.3 Functional Requirements

The system must allow new users to register accounts and automatically generate RSA-2048 key pairs upon registration. Registered users must be able to log in and log out securely using username and password authentication with session management. Authenticated users must be able to upload documents in common file formats including PDF, text, Word documents, and images. The system must generate digital signatures for uploaded documents using the signer's private RSA key and SHA-256 hashing. Users must be able to verify signatures on their documents and receive clear feedback indicating whether the document is authentic, tampered, or has an invalid signature. The system must maintain a dashboard displaying all user documents with their current status.

### 4.4 Non-Functional Requirements

The system must respond to user actions within two seconds under normal operating conditions. The cryptographic implementation must use industry-standard algorithms and padding schemes without custom or unverified cryptographic primitives. The user interface must be intuitive enough for users without technical or cryptographic background to complete signing and verification workflows without training. The database must maintain referential integrity between users, documents, and signatures, and the application architecture must separate presentation, business logic, and data layers to facilitate maintenance and future enhancement.

---

\newpage

## CHAPTER 5: SYSTEM DESIGN

### 5.1 System Architecture

The Document Signer System is architected using a layered approach with partial Model-View-Controller pattern that ensures clear separation of concerns across three primary layers. The View Layer comprises the HTML templates and CSS stylesheets that render the user interface, including the login page, registration form, document dashboard, signature verification screen, and document detail views. This layer is responsible solely for presenting information to the user and collecting input, without containing any business logic or database access code.

The Controller and Logic Layer is implemented through Django views and the dedicated cryptographic utility module. Django views handle HTTP request routing, form validation, authentication checks, and coordination between the view templates and the data layer. The crypto_utils module encapsulates all cryptographic operations including RSA key pair generation, document hashing, signature creation, and signature verification, ensuring that cryptographic logic is centralized and testable independent of the web framework.

The Database Layer uses SQLite through Django's Object-Relational Mapping system to persist user accounts, extended user profiles containing cryptographic keys, document records with file references and metadata, and digital signature records linking signers to documents with signature data and timestamps. Django's built-in authentication system manages user credentials while the custom UserProfile model extends each user with their RSA key pair.

### 5.2 Data Flow Diagram

At the context level, the data flow diagram shows a single external entity, the User, interacting with the Document Signer System through four primary data flows: login credentials, document files, signature requests, and verification results. The system processes these inputs and returns authentication tokens, signed document confirmations, verification status reports, and document management information.

At Level 1, the system decomposes into five major processes. The Login and Registration process accepts user credentials, validates them against the database, generates RSA key pairs for new users, and establishes authenticated sessions. The File Upload process receives document files from authenticated users, computes initial content hashes, stores files in the media directory, and creates document records in the database. The Signature Generation process retrieves document content and the signer's private key, computes the SHA-256 hash, applies RSA-PSS signing, and stores the resulting signature with its metadata. The Storage process manages all database read and write operations across the User, UserProfile, Document, and DigitalSignature entities. The Verification process retrieves a document and its stored signature, recomputes the content hash, verifies the signature cryptographically, compares hashes for tamper detection, and returns the verification result.

### 5.3 Entity-Relationship Model

The database schema consists of three primary entities in addition to Django's built-in User model. The User entity stores standard authentication fields including username, email, password hash, and account timestamps. The UserProfile entity maintains a one-to-one relationship with User and stores the PEM-encoded RSA private key and public key along with the profile creation timestamp. This design ensures that each user has exactly one cryptographic identity within the system.

The Document entity stores the document title, file path reference, SHA-256 content hash, status enumeration, upload timestamp, and a foreign key reference to the owning user. The status field tracks the document lifecycle through states of uploaded, signed, verified, and tampered. The DigitalSignature entity maintains a one-to-one relationship with Document and stores the base64-encoded signature data, the document hash at the time of signing, the signing algorithm identifier, the signing timestamp, and a foreign key reference to the signing user. This schema ensures that every signed document has exactly one signature record, and every signature is traceable to both a specific document and a specific signer.

### 5.4 Use Case Analysis

The primary actor in the system is the Registered User, who interacts with the system through six core use cases. The Register use case allows a new user to create an account, upon which the system automatically generates and stores an RSA-2048 key pair. The Login use case authenticates returning users and establishes a secure session. The Upload Document use case enables users to submit files with descriptive titles for signing. The Sign Document use case triggers the cryptographic signing pipeline on an uploaded document that has not yet been signed. The Verify Signature use case performs both cryptographic signature validation and tamper detection on a previously signed document. The View Document Details use case presents comprehensive information about a document including its metadata, hash values, and signature details.

---

\newpage

## CHAPTER 6: IMPLEMENTATION

### 6.1 Development Environment

The implementation was carried out using Visual Studio Code as the integrated development environment with the Python extension for syntax highlighting, linting, and debugging support. The project was initialized as a Django 4.2 application with a dedicated signer application module containing all business logic, models, views, and URL configurations. Dependencies were managed through a requirements.txt file specifying exact versions of Django, the cryptography library, and Pillow for image handling support.

### 6.2 Cryptographic Module

The cryptographic operations are centralized in the crypto_utils.py module, which provides a clean interface between the Django application and the underlying cryptography library. The generate_rsa_key_pair function creates a new RSA-2048 key pair using the standard public exponent of 65537 and the default cryptographic backend. The serialize_private_key and serialize_public_key functions convert key objects to PEM-encoded strings suitable for database storage, while the corresponding load functions reconstruct key objects from stored PEM strings.

The sign_document function implements the complete signing pipeline by first computing a SHA-256 hash of the document content using Python's hashlib module, then loading the signer's private key from its PEM representation, and finally applying the RSA-PSS signing operation with maximum salt length and SHA-256 as the hash algorithm. The function returns both the base64-encoded signature and the hexadecimal representation of the document hash for storage. The verify_document_signature function reverses this process by loading the public key, recomputing the document hash, decoding the stored signature, and invoking the RSA-PSS verification operation. The function returns a boolean indicating verification success, with any cryptographic exception resulting in a False return value to prevent information leakage about the nature of verification failures.

### 6.3 Application Logic

User registration is handled by the register_view function, which processes the Django UserCreationForm, creates a new User record upon valid submission, immediately generates an RSA key pair, and creates the associated UserProfile record storing both keys. The user is then automatically logged in and redirected to the dashboard. The login_view and logout_view functions manage session lifecycle using Django's built-in authentication framework.

Document upload is processed by the dashboard_view, which handles multipart form submissions containing both a document title and file. Upon successful validation, the view reads the uploaded file content, computes its SHA-256 hash, creates a Document record with status set to uploaded, and stores the file in the media/documents directory. The sign_document_view retrieves the document, verifies that it has not already been signed and belongs to the requesting user, reads the file content, invokes the signing function with the user's private key, creates a DigitalSignature record, and updates the document status to signed.

The verify_document_view implements the complete verification workflow by retrieving the document and its associated signature, reading the current file content, performing cryptographic signature verification using the user's public key, independently computing the current content hash and comparing it with the hash recorded at signing time, and determining whether the document is authentic, tampered, or has an invalid signature. The result is communicated through both status messages and visual indicators on the verification page.

### 6.4 User Interface

The user interface implements a modern dark theme designed for professional presentation and comfortable extended use. The login and registration pages feature a centered card layout with the system branding, shield iconography, and clean form fields against a gradient dark background. Authenticated users access the main application through a fixed sidebar navigation panel providing links to the dashboard, verification page, and logout action, with the current user's name displayed at the bottom of the sidebar.

The dashboard presents a two-column layout with the document upload form and system statistics on the left and a tabular listing of all user documents on the right. Each document row displays its identifier, title, color-coded status badge, upload timestamp, and action buttons for signing, verifying, and viewing details. The verification page provides a document selection form and a detailed results panel that displays document metadata, hash values, signature algorithm information, and a prominent result banner indicating verification outcome with appropriate iconography and color coding.

---

\newpage

## CHAPTER 7: TESTING AND RESULTS

### 7.1 Testing Methodology

The testing approach for this project encompasses both unit-level testing of individual cryptographic functions and integration testing of complete user workflows. Unit testing focused on verifying that the RSA key generation produces valid key pairs, that the sign and verify functions produce consistent results for unmodified documents, that verification correctly fails for documents modified after signing, and that verification correctly fails for signatures created with different key pairs. Integration testing validated the complete user journey from registration through document upload, signing, and verification using the web interface.

### 7.2 Test Cases and Results

The user registration test confirmed that new accounts are created successfully with automatically generated RSA-2048 key pairs stored in the UserProfile table. The login test verified that authenticated sessions are established correctly and unauthorized access to protected pages is redirected to the login screen. The document upload test demonstrated successful file storage with correct hash computation and database record creation with status set to uploaded.

The signature generation test produced valid RSA-PSS signatures for uploaded documents, with the document status updating to signed and all signature metadata including the algorithm identifier, timestamp, and document hash being recorded accurately. The signature verification test on unmodified signed documents returned a valid result with the status updating to verified, confirming both cryptographic signature validity and hash consistency. The tamper detection test involved modifying a signed document's file content and running verification, which correctly identified the document as tampered by detecting a mismatch between the current content hash and the hash recorded at signing time. The invalid signature test confirmed that verification fails appropriately when signature data is corrupted or when a different user's public key is used for verification.

### 7.3 System Screenshots

The implemented system presents a professional dark-themed interface across all functional screens. The login page displays the Document Signer System branding with username and password fields in a centered authentication card. The dashboard provides document upload functionality with a file chooser and title input alongside a comprehensive table of uploaded documents showing their signing status. The verification page presents detailed cryptographic information including SHA-256 hash values, signature algorithm, signing timestamp, and clear visual indicators for valid, tampered, and invalid verification results.

---

\newpage

## CHAPTER 8: CONCLUSION AND FUTURE SCOPE

### 8.1 Conclusion

This project has successfully demonstrated the design and implementation of a secure, practical digital signature system that addresses real-world challenges of document forgery and unauthorized modification in digital environments. By combining RSA-2048 cryptographic signing with SHA-256 integrity hashing within an accessible web-based interface, the Document Signer System bridges the gap between the theoretical security guarantees of public-key cryptography and the practical needs of users who require straightforward document authentication tools.

The system accomplishes its primary objectives of implementing secure digital signatures, ensuring data integrity through tamper detection, providing an intuitive user interface, and maintaining a well-structured database for all system entities. Through this implementation, the development team has gained substantial practical experience in software engineering, applied cryptography, database design, and system architecture, all of which represent essential competencies for professional software development careers.

The project validates the feasibility of building enterprise-grade security features using open-source tools and frameworks, demonstrating that robust document authentication does not require expensive commercial platforms or specialized hardware. The transparent cryptographic pipeline, where all operations are implemented in a dedicated utility module rather than hidden within proprietary libraries, provides educational value and auditability that commercial solutions typically do not offer.

### 8.2 Future Scope

Several enhancements have been identified that would extend the system's capabilities for production deployment. A web interface enhancement phase would add features such as drag-and-drop file upload, document preview, signature visualization overlays on PDF documents, and responsive mobile layouts. Multi-document batch signing would enable users to sign multiple documents in a single operation, improving efficiency for organizations processing large document volumes. Cloud deployment capability would involve containerizing the application with Docker, configuring MySQL or PostgreSQL for production database requirements, and deploying to cloud platforms such as AWS, Azure, or Google Cloud with proper SSL/TLS certificate management. Mobile application development would extend the signing and verification capabilities to Android and iOS platforms, enabling document authentication from smartphones and tablets. Integration with established public key infrastructure and certificate authorities would provide legally recognized digital signatures compliant with regulations such as the IT Act 2000 and eIDAS framework.

---

\newpage

## REFERENCES

1. Rivest, R. L., Shamir, A., & Adleman, L. (1978). A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. *Communications of the ACM*, 21(2), 120-126.

2. Diffie, W., & Hellman, M. (1976). New Directions in Cryptography. *IEEE Transactions on Information Theory*, 22(6), 644-654.

3. Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice* (7th ed.). Pearson Education.

4. National Institute of Standards and Technology. (2020). *Digital Signature Standard (DSS)*, FIPS PUB 186-4. U.S. Department of Commerce.

5. National Institute of Standards and Technology. (2020). *Secure Hash Standard (SHS)*, FIPS PUB 180-4. U.S. Department of Commerce.

6. Django Software Foundation. (2024). *Django Documentation* (Version 4.2). https://docs.djangoproject.com/

7. Python Cryptographic Authority. (2024). *Cryptography Library Documentation*. https://cryptography.io/

8. PKCS #1 v2.2: RSA Cryptography Specifications. RSA Laboratories.

9. Menezes, A. J., van Oorschot, P. C., & Vanstone, S. A. (2018). *Handbook of Applied Cryptography*. CRC Press.

10. Information Technology Act, 2000 (India). Ministry of Electronics and Information Technology, Government of India.

---

**END OF REPORT**
