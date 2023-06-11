import os
from supabase.client import create_client


class DB:

    def __init__(self) -> None:
        self.client = create_client(
            'https://jgeaqfizttebfqrstplw.supabase.co',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpnZWFxZml6dHRlYmZxcnN0cGx3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODM1MDQ0NDcsImV4cCI6MTk5OTA4MDQ0N30.qyU-nZq4B8Ty8EKWA9MZgrqPNADgB142GFCjl5BFFAQ'
        )

    def register_box(self, user: dict, box: dict) -> dict:
        """
        Registra una caja en la base de datos y la asocia con un usuario.

        :param user: los datos del usuario
        :param box: los datos de la caja
        """
        existing_box = self.__get_box(box['id'])
        if not existing_box:
            self.__create_user(
                user['id'], user['username']
            )
            self.__create_box(
                box=box,
                user_id=user['id']
            )
        else:
            return existing_box

    def set_password(self, box_id, password) -> None:
        """
        Establece una contraseña en una caja.

        :param box_id: id de la caja
        :param password: nueva contraseña de la caja
        """
        self.client.table('boxes').update({
            'password': password
        }).eq('id', box_id).execute()

    def __get_box(self, box_id) -> dict:
        """
        Metodo para obtener la informacion de una caja a partir de su id.
        """
        response = self.client.table('boxes').select(
            '*').eq('id', box_id).execute().data
        return None if not response else response[0]

    def __create_box(self, box: dict, user_id: int) -> None:
        self.client.table('boxes').insert({
            'id': box['id'],
            'password': box['password'],
            'user': user_id
        }).execute()

    def __create_user(self, user_id: int, username: str) -> None:
        """
        Crea un usuario en la tabla users a partir de los datos del chat de telegram.

        :param user_id: id del usuario
        :param username: nombre de usuario
        """
        self.client.table('users').insert({
            'id': user_id,
            'username': username
        }).execute()
