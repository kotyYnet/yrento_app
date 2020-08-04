from django.db import models


status = (
    ('volne' , "volne"),
    ('obsadene' , "obsadene")
)

aviability = (
    ('volne' , "volne"),
    ('v udrzbe' , "v udrzbe"),
    ('ynet' , "ynet")
)


class Categories(models.Model):

    name = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
            return self.name
    class Meta:
        managed = False
        db_table = 'Categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Dormitories(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    globalblock = models.IntegerField(db_column='globalBlock', blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'Dormitories'


class Items(models.Model):
    name = models.CharField(max_length=45)
    image = models.ImageField(upload_to='item/',blank=True, null=True )
    status = models.CharField(choices=status ,blank = True,null=True, max_length=10)
    aviability = models.CharField(choices=aviability ,blank = True,null=True, max_length=20)
    dormitory = models.ForeignKey(Dormitories, models.DO_NOTHING)
    price = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    interny_comment = models.TextField(blank=True, null=True)
    categories = models.ForeignKey(Categories, models.DO_NOTHING, db_column='Categories_id')
    quantity = models.FloatField(blank=True, null=True)

    def __str__(self):
         return self.name
    class Meta:
        
        db_table = 'Items'
        unique_together = (('id', 'dormitory'),)
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
