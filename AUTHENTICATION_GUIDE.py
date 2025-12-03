"""
Authentication API Testing Guide

AUTHENTICATION ENDPOINTS:
========================

1. REGISTER
-----------
POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123"
}

Response (201):
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "token": "abc123def456..."
}


2. LOGIN
--------
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword123"
}

Response (200):
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "token": "abc123def456..."
}


3. GET USER PROFILE
-------------------
GET http://localhost:8000/api/auth/profile/
Authorization: Token abc123def456...

Response (200):
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "discovered_items": [],
  "total_discovered": 0
}


4. LOGOUT
---------
POST http://localhost:8000/api/auth/logout/
Authorization: Token abc123def456...

Response (200):
{
  "message": "Logout successful"
}


USAGE IN FRONTEND:
==================

JavaScript example:
-------------------

// Register
async function register(username, email, password) {
  const response = await fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
}

// Login
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
}

// Get profile (requires token)
async function getProfile() {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/api/auth/profile/', {
    method: 'GET',
    headers: { 'Authorization': `Token ${token}` }
  });
  return await response.json();
}

// Use token for other API calls
async function combineItems(item1_name, item2_name) {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/api/combine/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    body: JSON.stringify({ item1_name, item2_name })
  });
  return await response.json();
}
"""
