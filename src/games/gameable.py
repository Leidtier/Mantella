from abc import ABC, abstractmethod
import logging
from typing import Any
import pandas as pd
from src.config_loader import ConfigLoader
from src.llm.sentence import sentence
from src.games.external_character_info import external_character_info
import src.utils as utils

class gameable(ABC):
    def __init__(self, path_to_character_df: str, mantella_software_game_folder_name: str):
        try:
            self.__character_df: pd.DataFrame = self.__get_character_df(path_to_character_df)
        except:
            logging.error(f'Unable to read / open {path_to_character_df}. If you have recently edited this file, please try reverting to a previous version. This error is normally due to using special characters, or saving the CSV in an incompatible format.')
            input("Press Enter to exit.")
        
        self.__mantella_software_game_folder_name: str = mantella_software_game_folder_name
    
    @property
    def Character_df(self) -> pd.DataFrame:
        return self.__character_df
    
    @property
    def Mantella_software_game_folder_name(self) -> str:
        return self.__mantella_software_game_folder_name
    
    def __get_character_df(self, file_name: str) -> pd.DataFrame:
        encoding = utils.get_file_encoding(file_name)
        character_df = pd.read_csv(file_name, engine='python', encoding=encoding)
        character_df = character_df.loc[character_df['voice_model'].notna()]

        return character_df
    
    @abstractmethod
    def load_external_character_info(self, id: str, name: str, race: str, gender: int, actor_voice_model_name: str)-> external_character_info:
        pass    

    @abstractmethod
    def prepare_sentence_for_game(self, queue_output: sentence, config: ConfigLoader):
        pass