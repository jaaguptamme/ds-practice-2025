# Documentation

System is designed as a microservices-based distributed system. Each service is responsible for a specific functionality, and the services communicate with each other using gRPC. The architecture is modular, constinting of components:

1. Frontend - A static HTML page served using Nginx.

2. Orchestrator - The central coordinator for the system.
Receives requests from the frontend and orchestrates calls to other backend services (e.g., fraud detection, transaction verification, suggestions) and combines the result.

3. Fraud Detection - Checks for fraudulent user data and credit card information.

4. Transaction Verification  - Verifies user data, billing addresses, and credit card details.

5. Suggestions - Provides book suggestions based on the items in the user's order.

6. Order Queue - Implements a queue to manage orders. Provides Enqueue and Dequeue operations for order processing.

7. Order Executor Service - Processes orders from the queue. Implements leader election to ensure mutual exclusion in a replicated environment.


# Connections Between Services:
1. Frontend → Orchestrator:
The frontend sends user order data to the orchestrator via HTTP (Flask API).

2. Orchestrator → Backend Services:
The orchestrator communicates with the fraud detection, transaction verification, and suggestions services using gRPC.
It also interacts with the order queue to enqueue orders.

3. Order Executor → Order Queue:
The order executor dequeues orders from the order queue for processing.

# Failure Modes
Service Failures:
If a backend service (e.g., fraud detection) fails, the orchestrator will handle the failure gracefully and return an appropriate error message to the frontend.

Data Consistency Issues:
Vector clocks are used to maintain consistency across services.

Leader Election Failures:
The Bully Algorithm ensures that a new leader is elected if the current leader fails. The algorithm selects the replica with the highest ID as the leader.

# Consistency Protocol
The system uses a **Primary-Based Protocol** to ensure consistency across the distributed databases. In this approach:
A **Primary Book Database Replica** is responsible for handling all write operations and propagating updates to the **Backup Replicas**.
Read operations can be performed on any replica.
The primary replica ensures sequential consistency by applying updates in the same order across all replicas.


# Distributed Commitment Protocol
The system uses the **Two-Phase Commit (2PC)** protocol to ensure consistency during distributed transactions. This protocol is implemented in the **Books Database** and **Payment Service** to handle critical operations like stock updates and payment processing.

### Two-Phase Commit Workflow:
1. **Prepare Phase**:
The main order executor sends a `Prepare` request to all books database and payment service.
Both of them check if can commit the transaction and responds with `Ready` or `Not Ready`.

2. **Commit Phase**:
If all backups respond with `Ready`, the order executor sends a `Commit` request to all backups.
If any backup responds with `Not Ready`, the order executor sends an `Abort` request to all backups.

This protocol ensures that transactions are either fully committed or fully rolled back, maintaining consistency across replicas.