import { ReactNode } from 'react';
import { Card, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';

interface PaymentMethodCardProps {
  id: string;
  title: string;
  description: string;
  icon: ReactNode;
  badge?: string;
  badgeVariant?: 'default' | 'secondary' | 'destructive' | 'outline';
  selected: boolean;
  disabled?: boolean;
  onClick: () => void;
}

export function PaymentMethodCard({
  id,
  title,
  description,
  icon,
  badge,
  badgeVariant = 'secondary',
  selected,
  disabled = false,
  onClick
}: PaymentMethodCardProps) {
  return (
    <Card 
      className={`cursor-pointer transition-all duration-200 ${
        selected 
          ? 'ring-2 ring-blue-500 border-blue-500 bg-blue-50' 
          : 'hover:border-gray-300 hover:shadow-sm'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      onClick={disabled ? undefined : onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              selected ? 'bg-blue-100' : 'bg-gray-100'
            }`}>
              {icon}
            </div>
            <div>
              <div className="font-medium text-gray-900">{title}</div>
              <div className="text-sm text-gray-500">{description}</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {badge && (
              <Badge variant={badgeVariant} className="text-xs">
                {badge}
              </Badge>
            )}
            <div className={`w-4 h-4 rounded-full border-2 ${
              selected 
                ? 'border-blue-500 bg-blue-500' 
                : 'border-gray-300'
            }`}>
              {selected && (
                <div className="w-full h-full rounded-full bg-white scale-50" />
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}