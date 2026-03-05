-- ─────────────────────────────────────────
--  Student Task Manager – Database Schema
--  Run this file in MySQL before starting app
-- ─────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS task_manager_db;
USE task_manager_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(50)  NOT NULL UNIQUE,
    email      VARCHAR(100) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(150) NOT NULL,
    description TEXT,
    priority    ENUM('High', 'Medium', 'Low') DEFAULT 'Medium',
    status      ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
    due_date    DATE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
