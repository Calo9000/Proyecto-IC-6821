from abc import ABC, abstractmethod

class ITransaccional(ABC):

    @abstractmethod
    def create(self, request):
        pass

    @abstractmethod
    def update(self, request, pk):
        pass

    @abstractmethod
    def delete(self, request, pk):
        pass

    @abstractmethod
    def get(self, request, pk):
        pass