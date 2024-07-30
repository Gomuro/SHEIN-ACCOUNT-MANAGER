from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

import logging

logger = logging.getLogger(__name__)

ResultType = TypeVar('ResultType')


@dataclass
class AlgorithmResult(Generic[ResultType]):
    """
    properties:
        - result: the result of the algorithm, type is ResultType in AlgorithmType[ResultType]. None if error
        - success: if algorithm finished without errors
        - exception: if success is False then the exception is error,
    caused while executing the algorithm
    """
    result: Optional[ResultType]
    success: bool
    exception: Optional[Exception]


class BasicAlgorithm(Generic[ResultType]):

    def __init__(self, driver):
        logger.info("BasicAlgorithm init")

        self.driver = driver
        self.logger = self.driver.logger

    def execute(self, **kwargs) -> AlgorithmResult:
        logger.info("BasicAlgorithm execute")
        """
        Executes itself algorithm and returns the result
        """
        try:
            result = self.start(**kwargs)
            logger.info("Result returned")
            return AlgorithmResult(
                result=result,
                success=True,
                exception=None,
            )

        except Exception as exception:
            logger.error(f"Error occurred while executing algorithm: {exception}")
            return AlgorithmResult(
                result=None,
                success=False,
                exception=exception,
            )

    @abstractmethod
    def start(self, **kwargs) -> ResultType:
        pass
