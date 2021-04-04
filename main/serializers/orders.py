"""сериалайзеры для модели Orders"""

from rest_framework import serializers

from main.models.ya_market.order.base import ItemPrice, Warehouse, Detail, Item, \
    InitialItem, PaymentOrder, DeliveryRegion, Order, Payment, Commission

from main.serializers.base import BaseListSerializer, BaseModelSerializer


class DeliveryRegionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='region_id', required=False)

    class Meta:
        model = DeliveryRegion
        fields = ['id', 'name']


class ItemPriceListSerializer(BaseListSerializer):
    key_fields = ['type']


class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = ['type', 'costPerItem', 'total']
        list_serializer_class = ItemPriceListSerializer


class WarehouseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='warehouse_id', required=False)

    class Meta:
        model = Warehouse
        fields = ['id', 'name']


class DetailListSerializer(BaseListSerializer):
    key_fields = ['itemStatus', 'stockType']


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ['itemCount', 'stockType', 'itemStatus', 'updateDate']
        list_serializer_class = DetailListSerializer


class ItemListSerializer(BaseListSerializer):
    key_fields = ['shopSku']


class ItemSerializer(BaseModelSerializer):
    prices = ItemPriceSerializer(many=True, required=False)
    warehouse = WarehouseSerializer(required=False)
    details = DetailSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        return 'item'

    class Meta:
        model = Item
        fields = ['offerName', 'marketSku', 'shopSku', 'count', 'prices', 'warehouse', 'details']
        list_serializer_class = ItemListSerializer


class InitialItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialItem
        fields = ['offerName', 'marketSku', 'shopSku', 'initialCount']
        list_serializer_class = ItemListSerializer


class PaymentOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='payment_order_id', required=False)

    class Meta:
        model = PaymentOrder
        fields = ['id', 'date']


class PaymentListSerializer(BaseListSerializer):
    key_fields = ['type', 'source']


class PaymentSerializer(BaseModelSerializer):
    paymentOrder = PaymentOrderSerializer(required=False)
    id = serializers.CharField(source='payment_id', required=False)

    @staticmethod
    def forward_name():
        return 'payment'

    class Meta:
        model = Payment
        fields = ['id', 'date', 'type', 'source', 'total', 'paymentOrder']
        list_serializer_class = PaymentListSerializer


class CommissionListSerializer(BaseListSerializer):
    key_fields = ['type']


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = ['type', 'actual', 'predicted']
        list_serializer_class = CommissionListSerializer


class OrderSerializer(BaseModelSerializer):
    id = serializers.IntegerField(source='order_id', required=False)
    deliveryRegion = DeliveryRegionSerializer(required=False)
    items = ItemSerializer(many=True, required=False)
    initialItems = InitialItemSerializer(many=True, required=False)
    payments = PaymentSerializer(many=True, required=False)
    commissions = CommissionSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        return 'order'

    class Meta:
        model = Order
        fields = ['id',
            'creationDate',
            'status',
            'statusUpdateDate',
            'partnerOrderId',
            'paymentType',
            'deliveryRegion',
            'items',
            'initialItems',
            'payments',
            'commissions'
        ]
