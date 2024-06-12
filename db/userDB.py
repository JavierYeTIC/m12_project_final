from db import clientPS
from model.User import User
from fastapi import FastAPI, HTTPException
from typing import Dict

from datetime import datetime


def registra(user: User):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO public.user (
                user_id, username, email, password, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
        """, (
            user.user_id, user.username, user.email, user.password,
            user.created_at, user.updated_at
        ))
        
        conn.commit()

    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail="Error registering user")
        
    finally:    
        conn.close()


def comprova( email:str, password:str):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM public.user WHERE email = %s", (email,))
        
        user_data = cur.fetchone()

        if user_data:
            stored_password = user_data[3]  
            if(password == stored_password):
                return True
       
    except Exception as e:
        print(f"ERROR: {e}")
        
    finally:    
        conn.close()
        
    return False


def load_users_from_db() -> Dict[str, User]:
    users = {}
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        
        cur.execute("SELECT user_id, username, email, password, created_at, updated_at FROM public.user")
        rows = cur.fetchall()
        
        for row in rows:
            user = User(
                user_id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                created_at=row[4],
                updated_at=row[5]
            )
            users[user.email] = user
        
    except Exception as e:
        print(f"ERROR: {e}")
        
    finally:
        conn.close()
    
    return users