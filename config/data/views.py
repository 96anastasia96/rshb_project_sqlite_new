from django.shortcuts import render

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.openapi import OpenApiResponse

from .models import Player, Equipment, Harvest, EquipmentShop, HarvestShop
from .serializers import PlayerSerializer, EquipmentSerializer, HarvestSerializer


# Create your views here.
player_status_codes = {
    status.HTTP_200_OK: OpenApiResponse(
        response=PlayerSerializer,
        description='ОК'
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        response=None,
        description='Неправильный запрос'
    ),
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=None,
        description='Пользователь не авторизован'
    ),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        response=None,
        description='Доступ запрещён'
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        response=None,
        description='Внутренняя ошибка сервера'
    )
}


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary='Получение списка всех объектов класса "Игрок"',
        tags=['Player'],
        request=PlayerSerializer,
        responses=player_status_codes
        )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Создание объекта класса "Игрок"',
        tags=['Player'],
        request=PlayerSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=PlayerSerializer,
                description='Создано'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        },
        examples=[
            OpenApiExample(
                name='Пример',
                value={
                    "name": "Doom Guy",
                    "gender": "Male",
                    "own_money": 5000,
                    "credit": 0,
                    "bank": 1,
                    "shop": 1
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary='Получение конкретного объекта класса "Игрок"',
        tags=['Player'],
        responses=player_status_codes
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary='Обновление информации об объекте класса "Игрок"',
        tags=['Player'],
        responses=player_status_codes)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @extend_schema(
        summary='Добавление информации к объекту класса "Игрок"',
        tags=['Player'],
        responses=player_status_codes,
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='Удаление объекта класса "Игрок"',
        tags=['Player'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description='OK'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


equipment_status_codes = {
    status.HTTP_200_OK: OpenApiResponse(
        response=EquipmentSerializer,
        description='ОК'
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        response=None,
        description='Неправильный запрос'
    ),
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=None,
        description='Пользователь не авторизован'
    ),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        response=None,
        description='Доступ запрещён'
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        response=None,
        description='Внутренняя ошибка сервера'
    )
}


class EquipmentViewSet(ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @extend_schema(
        summary='Получение списка всех объектов класса "Оборудование"',
        tags=['Equipment'],
        request=EquipmentSerializer,
        responses=equipment_status_codes
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Создание объекта класса "Оборудование"',
        tags=['Equipment'],
        request=EquipmentSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=EquipmentSerializer,
                description='Создано'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        },
        examples=[
            OpenApiExample(
                name='Пример',
                value={
                    "name": "BFG9000",
                    "description": "Big Fucking Gun",
                    "price": 666,
                    "availability": True,
                    "equipment_shop_id": 1,
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary='Получение конкретного объекта класса "Оборудование"',
        tags=['Equipment'],
        responses=equipment_status_codes
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary='Обновление информации об объекте класса "Оборудование"',
        tags=['Equipment'],
        responses=equipment_status_codes)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @extend_schema(
        summary='Добавление информации к объекту класса "Оборудование"',
        tags=['Equipment'],
        responses=equipment_status_codes,
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='Удаление объекта класса "Оборудование"',
        tags=['Equipment'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description='OK'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


harvest_status_codes = {
    status.HTTP_200_OK: OpenApiResponse(
        response=HarvestSerializer,
        description='ОК'
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        response=None,
        description='Неправильный запрос'
    ),
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=None,
        description='Пользователь не авторизован'
    ),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        response=None,
        description='Доступ запрещён'
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        response=None,
        description='Внутренняя ошибка сервера'
    )
}


class HarvestViewSet(ModelViewSet):
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary='Получение списка всех объектов класса "Урожай"',
        tags=['Harvest'],
        request=HarvestSerializer,
        responses=harvest_status_codes
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Создание объекта класса "Урожай"',
        tags=['Harvest'],
        request=HarvestSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=HarvestSerializer,
                description='Создано'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        },
        examples=[
            OpenApiExample(
                name='Пример',
                value={
                    "name": "Pineapple",
                    "description": "description of pineapple",
                    "price": 200,
                    "availability": True,
                    "gen_modified": False,
                    "harvest_shop_id": 1,
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary='Получение конкретного объекта класса "Урожай"',
        tags=['Harvest'],
        responses=harvest_status_codes
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary='Обновление информации об объекте класса "Урожай"',
        tags=['Harvest'],
        responses=harvest_status_codes)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @extend_schema(
        summary='Добавление информации к объекту класса "Урожай"',
        tags=['Harvest'],
        responses=harvest_status_codes,
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='Удаление объекта класса "Урожай"',
        tags=['Harvest'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description='OK'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

