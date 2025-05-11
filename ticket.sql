
CREATE DATABASE IF NOT EXISTS ticket;
USE ticket;


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);


CREATE TABLE IF NOT EXISTS resolved_tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_ticket_id INT NOT NULL,
    titre VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priorite VARCHAR(20) NOT NULL,
    date_creation DATETIME NOT NULL,
    date_resolution DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    resolved_by INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id)
);


CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priorite VARCHAR(20) NOT NULL,
    statut VARCHAR(20) DEFAULT 'En attente',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    assignee_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (assignee_id) REFERENCES users(id)
);

