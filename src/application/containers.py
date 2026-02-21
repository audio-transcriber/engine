from dependency_injector import containers, providers

from application.usecases import TranscriptionUseCase


class TranscriptionContainer(containers.DeclarativeContainer):
    whisper_container = providers.DependenciesContainer()
    minio_container = providers.DependenciesContainer()
    rabbitmq_container = providers.DependenciesContainer()

    usecase = providers.Factory(
        TranscriptionUseCase,
        providers.Factory(whisper_container.transcriptor),
        providers.Factory(minio_container.storage),
        providers.Factory(rabbitmq_container.producer),
    )
